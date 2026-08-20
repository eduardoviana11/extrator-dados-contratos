import os
import logging
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from models.schemas import ContractData

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_extractor_chain():
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        temperature=0,
        max_retries=2
    )

    structured_llm = llm.with_structured_output(ContractData)

    prompt = ChatPromptTemplate.from_messages([
        ("system", 
         "You are an expert legal AI assistant specializing in contract analysis."
         "Your sole purpose is to carefully read the provided contract text and extract"
         "the requested information accurately. If a specific piece of information is missing,"
         "follow the fallback instructions defined in the schema. "
         "Always provide a confidence score based on how explicitly the data is stated in the text."
         "IMPORTANT: Generate the 'summary' field and any text output in Brazilian Portuguese (pt-BR)."
        ),
        ("human", "Please extract the data from the following contract:\n\n{contract_text}")
    ])

    extractor_chain = prompt | structured_llm

    return extractor_chain

async def process_contract(contract_text: str) -> ContractData:
    try:
        logger.info("Iniciando extração de dados do contrato.")
        chain = get_extractor_chain()

        result = await chain.ainvoke({"contract_text": contract_text})

        logger.info(f"Extração concluída com score: {result.confidence_score}")
        return result
    except Exception as e:
        logger.error(f"Erro durante extração do contrato: {e}")
        raise e
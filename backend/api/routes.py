import io
import logging
from pypdf import PdfReader
from fastapi import APIRouter, UploadFile, File, HTTPException
from services.extractor import process_contract
from models.schemas import ExtractionResponse

logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/extract", response_model=ExtractionResponse)
async def extract_contract_data(file: UploadFile = File(...)):
    logger.info(f"Upload de arquivo recebido: {file.filename}")

    file_extension = file.filename.lower().split('.')[-1]

    if file_extension not in ['txt', 'pdf']:
        raise HTTPException(
            status_code=400,
            detail="Tipo de arquivo não suportado. Por favor, envie arquivos do tipo .txt ou .pdf."
        )

    try:
        content_bytes = await file.read()
        contract_text = ""

        if file_extension == 'txt':
            contract_text = content_bytes.decode('utf-8')

        elif file_extension == 'pdf':
            pdf_file_obj = io.BytesIO(content_bytes)
            pdf_reader = PdfReader(pdf_file_obj)

            for page in pdf_reader.pages:
                extracted_page_text = page.extract_text()
                if extracted_page_text:
                    contract_text += extracted_page_text + "\n"

        if not contract_text.strip():
            raise ValueError("Não foi possível extrair conteúdo legível do arquivo.")

        logger.info(f"Texto extraído com sucesso. Comprimento {len(contract_text)} caracteres.")

        extracted_data = await process_contract(contract_text)

        return ExtractionResponse(
            filename=file.filename,
            extracted_data=extracted_data,
            status="success"
        )
    
    except Exception as e:
        logger.error(f"Erro no endpoint /extract: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Um erro ocorreu no processamento do arquivo: {str(e)}"
        )

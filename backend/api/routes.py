import io
import logging
import asyncio
from typing import List
from pypdf import PdfReader
from fastapi import APIRouter, UploadFile, File, HTTPException
from services.extractor import process_contract
from models.schemas import ExtractionResponse, BatchExtractionResponse

logger = logging.getLogger(__name__)

router = APIRouter()

async def read_and_extract_file(file: UploadFile) -> ExtractionResponse:
    try:
        content_bytes = await file.read()
        file_extension = file.filename.lower().split('.')[-1]
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
             
        extracted_data = await process_contract(contract_text)
        
        return ExtractionResponse(
            filename=file.filename,
            extracted_data=extracted_data,
            status="success"
        )
    except Exception as e:
        logger.error(f"Error processing {file.filename}: {str(e)}")
        return ExtractionResponse(
            filename=file.filename,
            extracted_data={"contractor": "Error", "contractee": "Error", "total_value": 0.0, "signature_date": "Error", "has_penalty_clause": False, "summary": str(e), "confidence_score": 0},
            status="failed"
        )

@router.post("/extract", response_model=ExtractionResponse)
async def extract_contract_data(file: UploadFile = File(...)):
    if not file.filename.lower().endswith(('.txt', '.pdf')):
        raise HTTPException(
            status_code=400,
            detail="Tipo de arquivo não suportado. Por favor, envie arquivos do tipo .txt ou .pdf."
            )

    result = await read_and_extract_file(file)
    if result.status == "failed":
        raise HTTPException(status_code=500, detail=result.extracted_data.summary)
    return result

@router.post("/extract-batch", response_model=BatchExtractionResponse)
async def extract_batch_contracts(docs: List[UploadFile] = File(...)):
    logger.info(f"Upload de lote recebido: {len(docs)} arquivo(s)")

    tasks = [read_and_extract_file(doc) for doc in docs]

    results = await asyncio.gather(*tasks)

    successful = sum(1 for r in results if r.status == "success")

    return BatchExtractionResponse(
        total_processed=len(results),
        successful=successful,
        failed=len(results) - successful,
        results=results
    )
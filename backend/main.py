from fastapi import FastAPI
from api.routes import router as api_router

app = FastAPI(
    title="Auditor de Contratos",
    description="API para extração de dados estruturados de contratos usando LLMs",
    version="1.0.0"
)

app.include_router(api_router, prefix="/api/v1")

@app.get("/health")
async def health_check():
    return {"status": "ok", "message": "API is running OK"}
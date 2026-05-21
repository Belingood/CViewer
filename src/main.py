from fastapi import FastAPI
from fastapi.responses import JSONResponse

# Inicjalizacja głównej instancji aplikacji FastAPI
app = FastAPI(
    title="CViewer - System Ekstrakcji CV",
    description="API do przetwarzania i analizy dokumentów CV przy użyciu OCR.",
    version="0.1.0",
)

@app.get("/", tags=["Diagnostyka"])
async def root() -> dict[str, str]:
    """
    Podstawowy punkt końcowy do sprawdzania, czy serwer działa (Healthcheck).
    Zwraca prosty komunikat powitalny.
    """
    return {"message": "Serwer API Systemu Ekstrakcji CV działa poprawnie."}

@app.get("/api/v1/health", tags=["Diagnostyka"])
async def health_check() -> JSONResponse:
    """
    Endpoint diagnostyczny dla systemów monitorowania i CI/CD.
    """
    return JSONResponse(content={"status": "ok", "version": "0.1.0"})

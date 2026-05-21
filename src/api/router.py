from fastapi import APIRouter
from fastapi.responses import JSONResponse

# Inicjalizacja routera (bez globalnego stanu aplikacji)
api_router = APIRouter()

@api_router.get("/", tags=["Diagnostyka"])
async def root() -> dict[str, str]:
    """
    Podstawowy punkt końcowy do sprawdzania, czy serwer działa (Healthcheck).
    """
    return {"message": "Serwer API CViewer działa poprawnie."}

@api_router.get("/api/v1/health", tags=["Diagnostyka"])
async def health_check() -> JSONResponse:
    """
    Endpoint diagnostyczny (Healthcheck).
    """
    return JSONResponse(content={"status": "ok", "version": "0.1.0", "project": "CViewer"})

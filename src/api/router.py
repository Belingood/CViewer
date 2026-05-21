import io

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from fastapi.responses import JSONResponse
from PIL import Image

from src.schemas.cv import CVUploadResponse
from src.services.ocr_service import OCRService

api_router = APIRouter()


def get_ocr_service() -> OCRService:
    """
    Dostawca zależności (Dependency Provider) dla serwisu OCR.
    Zgodnie ze wzorcem Explicit Composition Root.
    """
    return OCRService()


@api_router.get("/", tags=["Diagnostyka"])
async def root() -> dict[str, str]:
    return {"message": "Serwer API CViewer działa poprawnie."}


@api_router.get("/api/v1/health", tags=["Diagnostyka"])
async def health_check() -> JSONResponse:
    return JSONResponse(content={"status": "ok", "version": "0.1.0", "project": "CViewer"})


@api_router.post("/api/v1/cv/upload/", response_model=CVUploadResponse, tags=["Dokumenty CV"])
async def upload_cv(
    file: UploadFile = File(...), ocr_service: OCRService = Depends(get_ocr_service)
) -> CVUploadResponse:
    """
    Endpoint do przesyłania i analizy dokumentów CV (obsługuje formaty obrazów: PNG, JPG).
    """
    # Sprawdzenie typu pliku
    if file.content_type not in ["image/jpeg", "image/png"]:
        raise HTTPException(
            status_code=400,
            detail="Nieobsługiwany format pliku. Proszę przesłać obraz w formacie JPG lub PNG.",
        )

    try:
        # Odczyt pliku do pamięci
        file_bytes = await file.read()
        image = Image.open(io.BytesIO(file_bytes))

        # Przetwarzanie obrazu przez serwis OCR
        extracted_data = ocr_service.process_image(image)

        return CVUploadResponse(
            filename=file.filename or "nieznany_plik",
            status="processed",
            extracted_data=extracted_data,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Błąd podczas przetwarzania obrazu: {str(e)}")

import io

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from fastapi.responses import JSONResponse
from PIL import Image
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.crud import create_cv_record
from src.db.database import get_db
from src.schemas.cv import CVUploadResponse
from src.services.ocr_service import OCRService

api_router = APIRouter()


def get_ocr_service() -> OCRService:
    return OCRService()


@api_router.get("/", tags=["Diagnostyka"])
async def root() -> dict[str, str]:
    return {"message": "Serwer API CViewer działa poprawnie."}


@api_router.get("/api/v1/health", tags=["Diagnostyka"])
async def health_check() -> JSONResponse:
    return JSONResponse(content={"status": "ok", "version": "0.1.0", "project": "CViewer"})


@api_router.post("/api/v1/cv/upload/", response_model=CVUploadResponse, tags=["Dokumenty CV"])
async def upload_cv(
    file: UploadFile = File(...),
    ocr_service: OCRService = Depends(get_ocr_service),
    db_session: AsyncSession = Depends(get_db),  # Wstrzykiwanie sesji bazy danych
) -> CVUploadResponse:
    """Endpoint do przesyłania, analizy i zapisu dokumentów CV."""
    allowed_types = ["image/jpeg", "image/png", "image/webp"]
    if file.content_type not in allowed_types:
        raise HTTPException(
            status_code=400,
            detail="Nieobsługiwany format pliku. "
            "Proszę przesłać obraz w formacie JPG, PNG lub WEBP.",
        )

    try:
        # 1. Odczyt i ekstrakcja (OCR + NLP)
        file_bytes = await file.read()
        image = Image.open(io.BytesIO(file_bytes))
        extracted_data = ocr_service.process_image(image)

        # 2. Zapis do bazy danych (PostgreSQL)
        saved_doc = await create_cv_record(
            session=db_session,
            filename=file.filename or "nieznany_plik",
            extracted_data=extracted_data,
        )

        # 3. Zwrócenie odpowiedzi (zawierającej ID z bazy)
        return CVUploadResponse(
            id=saved_doc.id,
            filename=saved_doc.filename,
            status=saved_doc.status,
            extracted_data=extracted_data,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Błąd przetwarzania: {str(e)}")

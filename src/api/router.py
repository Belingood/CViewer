import io

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from fastapi.responses import JSONResponse
from PIL import Image
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.crud import (
    create_cv_record,
    delete_cv_document,
    get_all_cvs,
    get_cv_by_id,
    update_candidate_data,
)
from src.db.database import get_db
from src.schemas.cv import (
    CandidateData,
    CandidateUpdateRequest,
    CVDetailResponse,
    CVListResponse,
    CVUploadResponse,
)
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


@api_router.get("/api/v1/cv/", response_model=list[CVListResponse], tags=["Dokumenty CV"])
async def list_cvs(db_session: AsyncSession = Depends(get_db)) -> list[CVListResponse]:
    """Zwraca listę wszystkich przesłanych dokumentów CV."""
    documents = await get_all_cvs(db_session)
    # Ręczna konwersja obiektów ORM na modele Pydantic dla zgodności z Mypy
    return [CVListResponse.model_validate(doc) for doc in documents]


@api_router.get("/api/v1/cv/{cv_id}", response_model=CVDetailResponse, tags=["Dokumenty CV"])
async def get_cv(cv_id: int, db_session: AsyncSession = Depends(get_db)) -> CVDetailResponse:
    """Zwraca szczegółowe informacje o wybranym dokumencie na podstawie jego ID."""
    document = await get_cv_by_id(db_session, cv_id)
    if not document:
        raise HTTPException(status_code=404, detail="Dokument o podanym ID nie został znaleziony.")
    return CVDetailResponse.model_validate(document)


@api_router.patch("/api/v1/cv/{cv_id}/candidate", response_model=CandidateData, tags=["Kandydaci"])
async def update_candidate(
    cv_id: int, update_data: CandidateUpdateRequest, db_session: AsyncSession = Depends(get_db)
) -> CandidateData:
    """Pozwala na ręczną korektę danych kandydata wyciągniętych przez OCR."""
    updated_candidate = await update_candidate_data(db_session, cv_id, update_data)
    if not updated_candidate:
        raise HTTPException(
            status_code=404, detail="Nie znaleziono danych kandydata dla tego dokumentu."
        )
    return CandidateData.model_validate(updated_candidate)


@api_router.delete(
    "/api/v1/cv/{cv_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Dokumenty CV"]
)
async def delete_cv(cv_id: int, db_session: AsyncSession = Depends(get_db)) -> None:
    """Trwale usuwa dokument oraz powiązane z nim dane kandydata z bazy danych."""
    success = await delete_cv_document(db_session, cv_id)
    if not success:
        raise HTTPException(status_code=404, detail="Dokument o podanym ID nie istnieje.")

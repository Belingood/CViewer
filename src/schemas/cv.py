from datetime import datetime

from pydantic import BaseModel, ConfigDict


class ExtractedCVData(BaseModel):
    email: str | None = None
    phone: str | None = None
    raw_text: str


class CVUploadResponse(BaseModel):
    id: int
    filename: str
    status: str
    extracted_data: ExtractedCVData


# --- ZAKTUALIZOWANE SCHEMATY PONIŻEJ ---


class CVListResponse(BaseModel):
    """Model dla elementu listy w widoku głównym (Dashboard)."""

    model_config = ConfigDict(from_attributes=True)  # Wymagane do konwersji z SQLAlchemy

    id: int
    filename: str
    upload_date: datetime
    status: str


class CandidateData(BaseModel):
    """Model reprezentujący dane kandydata w widoku szczegółowym."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    first_name: str | None = None
    last_name: str | None = None
    email: str | None = None
    phone: str | None = None


class CVDetailResponse(BaseModel):
    """Model szczegółowych informacji o pojedynczym CV."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    filename: str
    upload_date: datetime
    status: str
    raw_text: str | None = None
    candidate: CandidateData | None = None


class CandidateUpdateRequest(BaseModel):
    """Model do częściowej aktualizacji danych kandydata."""

    first_name: str | None = None
    last_name: str | None = None
    email: str | None = None
    phone: str | None = None

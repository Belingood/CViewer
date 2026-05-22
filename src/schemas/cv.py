from pydantic import BaseModel


class ExtractedCVData(BaseModel):
    """Model reprezentujący dane wyekstrahowane z dokumentu CV."""

    email: str | None = None
    phone: str | None = None
    raw_text: str


class CVUploadResponse(BaseModel):
    """Model odpowiedzi API po udanym przesłaniu i przetworzeniu dokumentu."""

    id: int
    filename: str
    status: str
    extracted_data: ExtractedCVData

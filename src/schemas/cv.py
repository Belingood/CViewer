from pydantic import BaseModel
from typing import Optional

class ExtractedCVData(BaseModel):
    """
    Model reprezentujący dane wyekstrahowane z dokumentu CV.
    """
    email: Optional[str] = None
    phone: Optional[str] = None
    raw_text: str

class CVUploadResponse(BaseModel):
    """
    Model odpowiedzi API po udanym przesłaniu i przetworzeniu dokumentu.
    """
    filename: str
    status: str
    extracted_data: ExtractedCVData

from sqlalchemy.ext.asyncio import AsyncSession

from src.db.models import Candidate, CVDocument
from src.schemas.cv import ExtractedCVData


async def create_cv_record(
    session: AsyncSession, filename: str, extracted_data: ExtractedCVData
) -> CVDocument:
    """
    Zapisuje informacje o przesłanym dokumencie oraz wyekstrahowane dane kandydata
    w bazie danych PostgreSQL w ramach pojedynczej transakcji.
    """
    # 1. Tworzenie rekordu dokumentu
    new_doc = CVDocument(filename=filename, raw_text=extracted_data.raw_text, status="processed")
    session.add(new_doc)

    # Flush wypycha zapytanie do bazy (INSERT), ale jeszcze nie zamyka transakcji.
    # Dzięki temu PostgreSQL generuje dla nas nowe ID (new_doc.id), które użyjemy niżej.
    await session.flush()

    # 2. Tworzenie powiązanego rekordu kandydata
    new_candidate = Candidate(
        document_id=new_doc.id, email=extracted_data.email, phone=extracted_data.phone
    )
    session.add(new_candidate)

    # 3. Zatwierdzenie całej transakcji (Commit)
    await session.commit()

    # Odświeżenie obiektu, aby mieć pewność, że zawiera wszystkie aktualne dane z bazy
    await session.refresh(new_doc)

    return new_doc

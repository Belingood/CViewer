from collections.abc import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.db.models import Candidate, CVDocument
from src.schemas.cv import CandidateUpdateRequest, ExtractedCVData


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
        document_id=new_doc.id,
        email=extracted_data.email,
        phone=extracted_data.phone,
        photo_path=extracted_data.photo_path,
    )
    session.add(new_candidate)

    # 3. Zatwierdzenie całej transakcji (Commit)
    await session.commit()

    # Odświeżenie obiektu, aby mieć pewność, że zawiera wszystkie aktualne dane z bazy
    await session.refresh(new_doc)

    return new_doc


async def get_all_cvs(session: AsyncSession) -> Sequence[CVDocument]:
    """Pobiera listę wszystkich dokumentów CV z bazy danych."""
    result = await session.execute(select(CVDocument).order_by(CVDocument.upload_date.desc()))
    return result.scalars().all()


async def get_cv_by_id(session: AsyncSession, cv_id: int) -> CVDocument | None:
    """
    Pobiera szczegóły CV wraz z powiązanymi danymi kandydata (Eager Loading).
    """
    result = await session.execute(
        select(CVDocument).options(selectinload(CVDocument.candidate)).where(CVDocument.id == cv_id)
    )
    return result.scalars().first()


async def update_candidate_data(
    session: AsyncSession, cv_id: int, update_data: CandidateUpdateRequest
) -> Candidate | None:
    """Aktualizuje wybrane pola kandydata (np. po ręcznej korekcie przez użytkownika)."""
    result = await session.execute(select(Candidate).where(Candidate.document_id == cv_id))
    candidate = result.scalars().first()

    if not candidate:
        return None

    # Aktualizacja tylko tych pól, które zostały przesłane w żądaniu (nie są None)
    update_dict = update_data.model_dump(exclude_unset=True)
    for key, value in update_dict.items():
        setattr(candidate, key, value)

    await session.commit()
    await session.refresh(candidate)
    return candidate


async def delete_cv_document(session: AsyncSession, cv_id: int) -> bool:
    """Usuwa dokument CV (kaskadowo usunie też kandydata dzięki ustawieniom w modelu)."""
    result = await session.execute(select(CVDocument).where(CVDocument.id == cv_id))
    document = result.scalars().first()

    if not document:
        return False

    await session.delete(document)
    await session.commit()
    return True

from __future__ import annotations

from datetime import datetime
from typing import Any

from sqlalchemy import DateTime, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from src.db.database import Base


class CVDocument(Base):
    """Model reprezentujący przesłany dokument CV w bazie danych."""

    __tablename__ = "cv_documents"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    filename: Mapped[str] = mapped_column(String, nullable=False)
    upload_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    raw_text: Mapped[str | None] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(String, default="pending")

    # Relacja One-to-One do ustrukturyzowanych danych kandydata
    # Dzięki 'annotations' nie potrzebujemy tutaj cudzysłowów wokół nazwy klasy
    candidate: Mapped[Candidate | None] = relationship(
        back_populates="document", uselist=False, cascade="all, delete-orphan"
    )


class Candidate(Base):
    """Model reprezentujący ustrukturyzowane dane wyciągnięte z CV."""

    __tablename__ = "candidates"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    document_id: Mapped[int] = mapped_column(ForeignKey("cv_documents.id", ondelete="CASCADE"))

    first_name: Mapped[str | None] = mapped_column(String, nullable=True)
    last_name: Mapped[str | None] = mapped_column(String, nullable=True)
    email: Mapped[str | None] = mapped_column(String, nullable=True)
    phone: Mapped[str | None] = mapped_column(String, nullable=True)

    # Przechowywanie dynamicznej listy w formacie JSONB
    skills: Mapped[dict[str, Any] | list[Any] | None] = mapped_column(JSONB, nullable=True)

    # Odniesienie do dokumentu
    document: Mapped[CVDocument] = relationship(back_populates="candidate")

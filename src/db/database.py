import os

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

DB_HOST = os.getenv("DB_HOST", "localhost")
DATABASE_URL = f"postgresql+asyncpg://cviewer_user:cviewer_password@{DB_HOST}:5432/cviewer_db"

engine = create_async_engine(DATABASE_URL, echo=True)

AsyncSessionLocal = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)


# Nowy standard SQLAlchemy 2.0 - w pełni wspierany przez Mypy
class Base(DeclarativeBase):
    """Bazowa klasa dla wszystkich modeli ORM."""

    pass


async def get_db() -> AsyncSession:  # type: ignore
    """Generator sesji bazy danych."""
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()

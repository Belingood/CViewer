import os
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from src.api.router import api_router
from src.db.database import Base, engine

# Importujemy modele, aby SQLAlchemy wiedziało o nich podczas tworzenia tabel
from src.db.models import Candidate, CVDocument  # noqa: F401


@asynccontextmanager
async def lifespan(app: FastAPI):  # type: ignore
    """
    Menedżer kontekstu zarządzający cyklem życia aplikacji (Lifespan).
    Kod przed yield wykonuje się podczas startu serwera, a po yield - podczas zamykania.
    """
    # Uruchomienie połączenia z bazą i asynchroniczne wygenerowanie tabel
    async with engine.begin() as conn:
        # run_sync pozwala na wykonanie synchronicznej metody metadata.create_all w środowisku async
        await conn.run_sync(Base.metadata.create_all)

    yield  # W tym momencie aplikacja działa i obsługuje żądania

    # Bezpieczne zamykanie połączeń z bazą danych przy wyłączaniu serwera
    await engine.dispose()


def create_app() -> FastAPI:
    """Explicit Composition Root dla aplikacji CViewer."""
    app = FastAPI(
        title="CViewer API",
        description="System ekstrakcji informacji z dokumentów CV oparty na OCR i NLP.",
        version="0.1.0",
        lifespan=lifespan,  # Podpięcie zdarzeń cyklu życia
    )

    # Zezwalamy na żądania z lokalnego serwera deweloperskiego Vite (Frontend)
    origins = [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],  # Pozwala na wszystkie metody: GET, POST, PATCH, DELETE
        allow_headers=["*"],  # Pozwala na wszystkie nagłówki
    )

    app.include_router(api_router)

    # Utworzenie głównego katalogu na pliki, jeśli nie istnieje
    os.makedirs("uploads", exist_ok=True)
    # Udostępnianie katalogu 'uploads' jako plików statycznych pod adresem URL '/uploads'
    app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

    return app


app = create_app()

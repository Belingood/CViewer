from fastapi import FastAPI

from src.api.router import api_router


def create_app() -> FastAPI:
    """
    Explicit Composition Root dla aplikacji CViewer.
    W tym miejscu odbywa się inicjalizacja aplikacji, rejestracja routerów
    oraz wstrzykiwanie zależności (Dependency Injection).
    """
    # 1. Tworzenie instancji aplikacji
    app = FastAPI(
        title="CViewer API",
        description="System ekstrakcji informacji z dokumentów CV oparty na OCR i NLP.",
        version="0.1.0",
    )

    # 2. Rejestracja endpointów (Routerów)
    app.include_router(api_router)

    # 3. W przyszłości: konfiguracja połączenia z bazą danych i wstrzykiwanie serwisów
    # np. app.dependency_overrides[Database] = setup_database(...)

    return app

# Główna instancja aplikacji wywoływana przez serwer Uvicorn
app = create_app()

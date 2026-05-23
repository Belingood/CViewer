from unittest.mock import AsyncMock, patch

from fastapi.testclient import TestClient

from src.main import app

# Inicjalizacja klienta testowego (bez uruchamiania prawdziwego serwera Uvicorn)
client = TestClient(app)


def test_health_check_endpoint() -> None:
    """Test weryfikujący punkt diagnostyczny API."""
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"
    assert response.json()["project"] == "CViewer"


@patch("src.api.router.get_all_cvs", new_callable=AsyncMock)
def test_get_all_cvs(mock_get_all_cvs: AsyncMock) -> None:
    """
    Test pobierania listy CV.
    Używamy 'patch' do zaślepienia (Mocking) funkcji bazodanowej 'get_all_cvs'.
    """

    # Symulacja zwróconych danych z bazy (jako słowniki lub obiekty z atrybutami)
    class MockCV:
        id = 1
        filename = "test_cv.pdf"
        upload_date = "2026-05-23T10:00:00Z"
        status = "processed"

    mock_get_all_cvs.return_value = [MockCV()]

    response = client.get("/api/v1/cv/")

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["filename"] == "test_cv.pdf"
    assert data[0]["id"] == 1


@patch("src.api.router.delete_cv_document", new_callable=AsyncMock)
def test_delete_cv_success(mock_delete_cv: AsyncMock) -> None:
    """Test poprawnego usuwania dokumentu CV."""
    # Symulacja udanego usunięcia z bazy
    mock_delete_cv.return_value = True

    response = client.delete("/api/v1/cv/1")

    # Przy poprawnym usunięciu (REST) oczekujemy kodu 204 No Content
    assert response.status_code == 204


@patch("src.api.router.delete_cv_document", new_callable=AsyncMock)
def test_delete_cv_not_found(mock_delete_cv: AsyncMock) -> None:
    """Test usuwania dokumentu, który nie istnieje w bazie (Błąd 404)."""
    # Symulacja sytuacji, w której rekord nie istnieje
    mock_delete_cv.return_value = False

    response = client.delete("/api/v1/cv/999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Dokument o podanym ID nie istnieje."

from fastapi.testclient import TestClient

from src.main import app

# Inicjalizacja klienta testowego
client = TestClient(app)

def test_root_endpoint() -> None:
    """
    Test weryfikujący poprawne działanie głównego endpointu (/).
    Oczekiwany kod odpowiedzi to 200 OK.
    """
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Serwer API Systemu Ekstrakcji CV działa poprawnie."}

def test_health_check_endpoint() -> None:
    """
    Test weryfikujący działanie endpointu diagnostycznego (/api/v1/health).
    """
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "version": "0.1.0"}

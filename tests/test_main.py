from fastapi.testclient import TestClient
from src.main import app

# Inicjalizacja klienta testowego
client = TestClient(app)

def test_root_endpoint() -> None:
    """Test głównego punktu końcowego."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Serwer API CViewer działa poprawnie."}

def test_health_check_endpoint() -> None:
    """Test diagnostyczny aplikacji (Healthcheck)."""
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "version": "0.1.0", "project": "CViewer"}

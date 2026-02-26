from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health_endpoint_shape() -> None:
    response = client.get("/health")

    assert response.status_code == 200
    payload = response.json()
    assert set(payload.keys()) == {"status", "db", "redis"}
    assert payload["status"] in {"ok", "degraded"}

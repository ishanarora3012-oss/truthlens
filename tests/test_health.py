"""Smoke tests for API composition."""

from fastapi.testclient import TestClient

from backend.main import app


def test_health_check_returns_ok() -> None:
    """The liveness endpoint remains available."""
    with TestClient(app) as client:
        response = client.get("/api/v1/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

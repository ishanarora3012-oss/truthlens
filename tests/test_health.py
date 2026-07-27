"""API integration tests for the runnable baseline."""

import os

os.environ["TRUTHLENS_DATABASE_URL"] = "sqlite:///./test_truthlens.db"

from backend.main import app
from fastapi.testclient import TestClient


def test_health_check_returns_ok() -> None:
    """The liveness endpoint remains available."""
    with TestClient(app) as client:
        response = client.get("/api/v1/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_check_returns_evidence_grounded_assessment() -> None:
    """Supported answer receives evidence and a complete explanation."""
    with TestClient(app) as client:
        response = client.post(
            "/api/v1/check",
            json={
                "question": "What is the capital of France?",
                "answer": "Paris is the capital of France.",
                "context": ["Paris is the capital and most populous city of France."],
            },
        )

    body = response.json()
    assert response.status_code == 200
    assert body["hallucination"] is False
    assert body["evidence"]
    assert body["explanation"]["token_attributions"]


def test_check_flags_entity_mismatch() -> None:
    """Conflicting named entities are flagged against trusted context."""
    with TestClient(app) as client:
        response = client.post(
            "/api/v1/check",
            json={
                "question": "What is the capital of France?",
                "answer": "Lyon is the capital of France.",
                "context": ["Paris is the capital and most populous city of France."],
            },
        )

    assert response.status_code == 200
    assert response.json()["hallucination"] is True


def test_benchmark_evaluates_each_supplied_model_answer() -> None:
    """Benchmark endpoint preserves each caller-supplied model name."""
    with TestClient(app) as client:
        response = client.post(
            "/api/v1/benchmark",
            json={
                "question": "What is the capital of France?",
                "context": ["Paris is the capital and most populous city of France."],
                "responses": {
                    "accurate": "Paris is the capital of France.",
                    "incorrect": "Lyon is the capital.",
                },
            },
        )

    assert response.status_code == 200
    assert {item["model"] for item in response.json()["results"]} == {"accurate", "incorrect"}

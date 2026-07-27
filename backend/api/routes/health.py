"""Operational health routes."""

from fastapi import APIRouter

from backend.api.schemas import HealthResponse

router = APIRouter(tags=["operations"])


@router.get("/health", response_model=HealthResponse, summary="Check API liveness")
def health_check() -> HealthResponse:
    """Return a lightweight liveness result."""
    return HealthResponse(status="ok")

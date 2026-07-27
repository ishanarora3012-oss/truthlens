"""Hallucination assessment routes."""

from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.api.schemas import CheckRequest, CheckResponse
from backend.config.settings import get_settings
from backend.database.session import get_session
from backend.services.hallucination_service import HallucinationService

router = APIRouter(tags=["assessment"])


@router.post(
    "/check",
    response_model=CheckResponse,
    summary="Assess an answer for hallucination",
)
def check_answer(
    payload: CheckRequest,
    session: Annotated[Session, Depends(get_session)],
) -> CheckResponse:
    """Assess an answer with the evidence-grounded baseline detector."""
    return HallucinationService(get_settings(), session).assess(payload)

"""Hallucination assessment routes."""

from fastapi import APIRouter, HTTPException, status

from backend.api.schemas import CheckRequest, CheckResponse

router = APIRouter(tags=["assessment"])


@router.post(
    "/check",
    response_model=CheckResponse,
    status_code=status.HTTP_501_NOT_IMPLEMENTED,
    summary="Assess an answer for hallucination",
)
def check_answer(payload: CheckRequest) -> CheckResponse:
    """Reserve the Phase 1 hallucination-assessment contract.

    TODO: orchestrate retrieval, semantic comparison, classifier inference,
    confidence calibration, and explanation generation.
    """
    del payload
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Hallucination assessment pipeline has not been implemented yet.",
    )

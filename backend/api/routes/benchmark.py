"""Comparable multi-model assessment routes."""

from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.api.schemas import BenchmarkRequest, BenchmarkResponse, BenchmarkResult, CheckRequest
from backend.config.settings import get_settings
from backend.database.session import get_session
from backend.services.hallucination_service import HallucinationService

router = APIRouter(tags=["benchmarking"])


@router.post(
    "/benchmark", response_model=BenchmarkResponse, summary="Benchmark model answers on one prompt"
)
def benchmark_answers(
    payload: BenchmarkRequest,
    session: Annotated[Session, Depends(get_session)],
) -> BenchmarkResponse:
    """Assess all supplied model answers under identical question and context."""
    service = HallucinationService(get_settings(), session)
    results = [
        BenchmarkResult(
            model=model,
            assessment=service.assess(
                CheckRequest(question=payload.question, answer=answer, context=payload.context),
                persist=False,
            ),
        )
        for model, answer in payload.responses.items()
    ]
    return BenchmarkResponse(question=payload.question, results=results)

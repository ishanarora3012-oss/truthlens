"""Persisted assessment history routes."""

from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from backend.api.schemas import HistoryItem
from backend.database.repository import AssessmentRepository
from backend.database.session import get_session

router = APIRouter(tags=["history"])


@router.get("/history", response_model=list[HistoryItem], summary="List recent assessments")
def list_history(
    session: Annotated[Session, Depends(get_session)],
    limit: Annotated[int, Query(ge=1, le=100)] = 20,
) -> list[HistoryItem]:
    """Return persisted assessments for the dashboard history panel."""
    return [
        HistoryItem.model_validate(record)
        for record in AssessmentRepository(session).list_recent(limit)
    ]

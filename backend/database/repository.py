"""Repository implementations for persisted application history."""

from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.database.models import AssessmentRecord


class AssessmentRepository:
    """Encapsulate assessment persistence queries."""

    def __init__(self, session: Session) -> None:
        self._session = session

    def add(self, record: AssessmentRecord) -> AssessmentRecord:
        """Persist and refresh an assessment record."""
        self._session.add(record)
        self._session.commit()
        self._session.refresh(record)
        return record

    def list_recent(self, limit: int = 20) -> list[AssessmentRecord]:
        """Return most recent assessments first."""
        statement = (
            select(AssessmentRecord).order_by(AssessmentRecord.created_at.desc()).limit(limit)
        )
        return list(self._session.scalars(statement))

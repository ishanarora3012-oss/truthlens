"""Database entities for assessments and benchmark runs."""

from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy import JSON, DateTime, Float, String, Text, Uuid, func
from sqlalchemy.orm import Mapped, mapped_column

from backend.database.base import Base


class AssessmentRecord(Base):
    """Persisted result of a single hallucination assessment."""

    __tablename__ = "assessments"

    id: Mapped[UUID] = mapped_column(Uuid, primary_key=True, default=uuid4)
    question: Mapped[str] = mapped_column(Text)
    answer: Mapped[str] = mapped_column(Text)
    hallucination_score: Mapped[float] = mapped_column(Float)
    confidence: Mapped[float] = mapped_column(Float)
    hallucination: Mapped[bool]
    reason: Mapped[str] = mapped_column(String(500))
    evidence: Mapped[list[dict[str, object]]] = mapped_column(JSON, default=list)
    explanation: Mapped[dict[str, object]] = mapped_column(JSON, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

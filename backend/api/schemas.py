"""Pydantic request and response contracts for the HTTP API."""

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class CheckRequest(BaseModel):
    """A question and candidate answer to assess."""

    question: str = Field(
        min_length=1, max_length=10_000, examples=["What is the capital of France?"]
    )
    answer: str = Field(
        min_length=1, max_length=50_000, examples=["Paris is the capital of France."]
    )
    context: list[str] = Field(
        default_factory=list,
        max_length=20,
        description="Optional trusted passages supplied by the caller.",
    )


class EvidenceItem(BaseModel):
    """A retrieved or caller-provided evidence passage."""

    id: str
    title: str
    content: str
    source: str | None = None
    relevance: float = Field(ge=0, le=1)


class TokenAttribution(BaseModel):
    """A token-level explanation signal."""

    token: str
    contribution: float = Field(ge=-1, le=1)
    label: str


class Explanation(BaseModel):
    """Human-readable and machine-readable assessment explanation."""

    summary: str
    supported_claims: list[str] = Field(default_factory=list)
    unsupported_claims: list[str] = Field(default_factory=list)
    token_attributions: list[TokenAttribution] = Field(default_factory=list)
    method: str


class CheckResponse(BaseModel):
    """The normalized result of a hallucination assessment."""

    hallucination: bool
    confidence: float = Field(ge=0, le=100)
    reason: str
    hallucination_score: float = Field(ge=0, le=1)
    semantic_similarity: float = Field(ge=0, le=1)
    evidence: list[EvidenceItem] = Field(default_factory=list)
    explanation: Explanation
    assessment_id: UUID | None = None


class HealthResponse(BaseModel):
    """Liveness response."""

    status: str


class HistoryItem(BaseModel):
    """Compact persisted assessment used by the dashboard history view."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    question: str
    answer: str
    hallucination: bool
    confidence: float
    hallucination_score: float
    reason: str
    created_at: datetime


class BenchmarkRequest(BaseModel):
    """Answers from several LLMs to one identical question."""

    question: str = Field(min_length=1, max_length=10_000)
    responses: dict[str, str] = Field(min_length=1, description="Model name to answer mapping.")
    context: list[str] = Field(default_factory=list, max_length=20)


class BenchmarkResult(BaseModel):
    """Assessment result for one model in a benchmark run."""

    model: str
    assessment: CheckResponse


class BenchmarkResponse(BaseModel):
    """Comparable assessment results for an identical prompt."""

    question: str
    results: list[BenchmarkResult]

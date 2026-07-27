"""Pydantic request and response contracts for the HTTP API."""

from pydantic import BaseModel, Field


class CheckRequest(BaseModel):
    """A question and candidate answer to assess."""

    question: str = Field(min_length=1, max_length=10_000, examples=["What is the capital of France?"])
    answer: str = Field(min_length=1, max_length=50_000, examples=["Paris is the capital of France."])


class CheckResponse(BaseModel):
    """The normalized result of a hallucination assessment."""

    hallucination: bool
    confidence: float = Field(ge=0, le=100)
    reason: str


class HealthResponse(BaseModel):
    """Liveness response."""

    status: str

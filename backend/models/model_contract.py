"""Shared contracts for classifier model adapters."""

from typing import Protocol


class ClassifierAdapter(Protocol):
    """Interface implemented by every classifier family."""

    def predict(self, question: str, answer: str) -> float:
        """Return a hallucination probability in the inclusive range [0, 1]."""

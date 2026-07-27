"""Hallucination assessment orchestration contract."""

from backend.api.schemas import CheckRequest, CheckResponse


class HallucinationService:
    """Coordinate the end-to-end hallucination detection pipeline."""

    def assess(self, request: CheckRequest) -> CheckResponse:
        """Assess a response against retrieved evidence.

        TODO: implement the pipeline once ML components are available.
        """
        raise NotImplementedError

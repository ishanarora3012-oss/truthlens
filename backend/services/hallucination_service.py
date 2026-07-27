"""Hallucination assessment use case orchestration."""

from sqlalchemy.orm import Session

from backend.api.schemas import CheckRequest, CheckResponse, EvidenceItem
from backend.config.settings import Settings
from backend.database.models import AssessmentRecord
from backend.database.repository import AssessmentRepository
from backend.explainability.lime_explainer import LimeExplainer
from backend.services.assessment_engine import EvidenceGroundedAssessmentEngine
from backend.services.evidence_retrieval import EvidenceRetriever


class HallucinationService:
    """Coordinate the end-to-end hallucination detection pipeline.

    ``session`` is optional because pure evaluation (offline dataset
    benchmarking) never persists a result and should not require a database.
    """

    def __init__(self, settings: Settings, session: Session | None = None) -> None:
        self._session = session
        self._retriever = EvidenceRetriever(settings.knowledge_base_path)
        self._engine = EvidenceGroundedAssessmentEngine(settings.hallucination_threshold)
        self._explainer = LimeExplainer()

    def assess(self, request: CheckRequest, persist: bool = True) -> CheckResponse:
        """Assess a response against evidence and optionally persist the result."""
        documents = self._retriever.retrieve(request.question, request.answer, request.context)
        result = self._engine.assess(request.answer, documents)
        explanation = self._explainer.explain(
            result.features.supported_tokens,
            result.features.unsupported_tokens,
            result.reason,
        )
        evidence = [
            EvidenceItem(
                id=document.id,
                title=document.title,
                content=document.content,
                source=document.source,
                relevance=document.relevance,
            )
            for document in documents
        ]
        response = CheckResponse(
            hallucination=result.hallucination,
            confidence=result.confidence,
            reason=result.reason,
            hallucination_score=result.hallucination_score,
            semantic_similarity=result.features.semantic_similarity,
            evidence=evidence,
            explanation=explanation,
        )
        if not persist:
            return response
        if self._session is None:
            raise RuntimeError("Persisting an assessment requires a database session.")
        record = AssessmentRepository(self._session).add(
            AssessmentRecord(
                question=request.question,
                answer=request.answer,
                hallucination=response.hallucination,
                confidence=response.confidence,
                hallucination_score=response.hallucination_score,
                reason=response.reason,
                evidence=[item.model_dump(mode="json") for item in evidence],
                explanation=explanation.model_dump(mode="json"),
            )
        )
        return response.model_copy(update={"assessment_id": record.id})

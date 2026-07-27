"""Transparent evidence-grounded baseline hallucination detector."""

import re
from dataclasses import dataclass

from backend.services.evidence_retrieval import EvidenceDocument
from backend.services.semantic_similarity import cosine_similarity, tokenize


@dataclass(frozen=True, slots=True)
class AssessmentFeatures:
    """Intermediate signals used to calculate an assessment."""

    semantic_similarity: float
    answer_coverage: float
    numeric_mismatch: bool
    named_entity_mismatch: bool
    unsupported_tokens: list[str]
    supported_tokens: list[str]


@dataclass(frozen=True, slots=True)
class EngineResult:
    """Output of the transparent baseline assessment engine."""

    hallucination: bool
    hallucination_score: float
    confidence: float
    reason: str
    features: AssessmentFeatures


class EvidenceGroundedAssessmentEngine:
    """Score unsupported answer claims against retrieved evidence.

    This is a transparent baseline, not a universal fact verifier. It reports
    uncertainty whenever no relevant evidence can be retrieved.
    """

    def __init__(self, threshold: float) -> None:
        self._threshold = threshold

    def assess(self, answer: str, evidence: list[EvidenceDocument]) -> EngineResult:
        """Assess one answer using semantic and numeric support signals."""
        if not evidence:
            features = AssessmentFeatures(0.0, 0.0, False, False, tokenize(answer)[:12], [])
            return EngineResult(
                False, 0.5, 25.0, "Insufficient evidence to verify the answer.", features
            )

        evidence_text = " ".join(item.content for item in evidence)
        answer_tokens = tokenize(answer)
        evidence_tokens = set(tokenize(evidence_text))
        supported = [token for token in answer_tokens if token in evidence_tokens]
        unsupported = [token for token in answer_tokens if token not in evidence_tokens]
        coverage = len(supported) / len(answer_tokens) if answer_tokens else 0.0
        similarity = cosine_similarity(answer, evidence_text)
        answer_numbers = {token for token in answer_tokens if token.isdigit()}
        evidence_numbers = {token for token in evidence_tokens if token.isdigit()}
        numeric_mismatch = bool(answer_numbers - evidence_numbers)
        answer_entities = {item.lower() for item in re.findall(r"\b[A-Z][a-z]{2,}\b", answer)}
        evidence_entities = {
            item.lower() for item in re.findall(r"\b[A-Z][a-z]{2,}\b", evidence_text)
        }
        named_entity_mismatch = bool(answer_entities - evidence_entities)
        score = (1 - coverage) * 0.55 + (1 - similarity) * 0.30
        score += 0.15 if numeric_mismatch else 0
        score += 0.35 if named_entity_mismatch else 0
        score = round(min(max(score, 0.0), 1.0), 4)
        hallucination = score >= self._threshold
        confidence = round(
            min(99.0, 45.0 + abs(score - self._threshold) * 85.0 + coverage * 10.0), 1
        )
        if numeric_mismatch:
            reason = "Numeric claim is not supported by the retrieved evidence."
        elif named_entity_mismatch:
            reason = "Named entity in the answer does not match the retrieved evidence."
        elif hallucination:
            reason = "The answer contains material terms not supported by retrieved evidence."
        else:
            reason = "The answer is substantially supported by retrieved evidence."
        features = AssessmentFeatures(
            similarity,
            round(coverage, 4),
            numeric_mismatch,
            named_entity_mismatch,
            unsupported,
            supported,
        )
        return EngineResult(hallucination, score, confidence, reason, features)

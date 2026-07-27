"""RoBERTa inference entry point."""

from pathlib import Path

from backend.models.transformer_classifier import predict_probability


def predict(question: str, answer: str, checkpoint_dir: str = "artifacts/roberta") -> float:
    """Predict hallucination probability with a saved RoBERTa classifier."""
    return predict_probability(question, answer, Path(checkpoint_dir))

"""BERT training entry point."""

from backend.models.bert.config import make_config
from backend.models.transformer_classifier import TrainingResult, train_classifier


def train(dataset_path: str, output_dir: str = "artifacts/bert") -> TrainingResult:
    """Fine-tune BERT from a labelled question/answer CSV."""
    return train_classifier(make_config(dataset_path, output_dir))

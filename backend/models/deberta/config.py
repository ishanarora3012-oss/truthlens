"""DeBERTa classifier configuration."""

from pathlib import Path

from backend.models.transformer_classifier import TransformerTrainingConfig

MODEL_NAME = "microsoft/deberta-v3-base"


def make_config(
    dataset_path: str, output_dir: str = "artifacts/deberta"
) -> TransformerTrainingConfig:
    """Build DeBERTa fine-tuning configuration from user-supplied paths."""
    return TransformerTrainingConfig(MODEL_NAME, Path(dataset_path), Path(output_dir))

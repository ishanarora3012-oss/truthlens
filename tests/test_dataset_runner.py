"""Tests for the offline dataset benchmarking harness."""

from pathlib import Path

import pytest
from backend.config.settings import get_settings
from backend.evaluation.dataset_runner import load_dataset, run_dataset_evaluation

SAMPLE_DATASET = Path(__file__).parent.parent / "experiments" / "sample_dataset.csv"


def test_load_dataset_rejects_missing_columns(tmp_path: Path) -> None:
    """A dataset missing a required column should fail fast with a clear error."""
    dataset_path = tmp_path / "invalid.csv"
    dataset_path.write_text("question,answer\nWhat?,Because.\n", encoding="utf-8")

    with pytest.raises(ValueError, match="missing required columns"):
        load_dataset(dataset_path)


def test_run_dataset_evaluation_scores_the_sample_dataset() -> None:
    """The sample dataset should be evaluated end to end with sane metrics."""
    report = run_dataset_evaluation(SAMPLE_DATASET, get_settings())

    assert report.sample_count == 10
    assert 0.0 <= report.metrics.accuracy <= 1.0
    assert report.mean_latency_ms > 0
    assert report.p95_latency_ms >= 0

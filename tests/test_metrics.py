"""Evaluation metric tests."""

from backend.evaluation.metrics import compute_classification_metrics


def test_classification_metrics_are_calculated_correctly() -> None:
    """Metrics should have expected values for a small binary example."""
    result = compute_classification_metrics([True, True, False, False], [True, False, True, False])

    assert result.accuracy == 0.5
    assert result.precision == 0.5
    assert result.recall == 0.5
    assert result.f1 == 0.5

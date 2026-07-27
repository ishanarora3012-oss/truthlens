"""Dependency-light classification metric calculations."""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ClassificationMetrics:
    """Binary-classification metrics for a labelled benchmark set."""

    accuracy: float
    precision: float
    recall: float
    f1: float


def compute_classification_metrics(
    labels: list[bool], predictions: list[bool]
) -> ClassificationMetrics:
    """Compute accuracy, precision, recall, and F1 from boolean labels."""
    if not labels or len(labels) != len(predictions):
        raise ValueError("labels and predictions must be non-empty lists of equal length")
    true_positive = sum(
        label and prediction for label, prediction in zip(labels, predictions, strict=True)
    )
    false_positive = sum(
        not label and prediction for label, prediction in zip(labels, predictions, strict=True)
    )
    false_negative = sum(
        label and not prediction for label, prediction in zip(labels, predictions, strict=True)
    )
    accuracy = sum(
        label == prediction for label, prediction in zip(labels, predictions, strict=True)
    ) / len(labels)
    precision = (
        true_positive / (true_positive + false_positive) if true_positive + false_positive else 0.0
    )
    recall = (
        true_positive / (true_positive + false_negative) if true_positive + false_negative else 0.0
    )
    f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0.0
    return ClassificationMetrics(
        round(accuracy, 4), round(precision, 4), round(recall, 4), round(f1, 4)
    )

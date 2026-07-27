"""Offline benchmark harness for scoring a labeled dataset end to end."""

import csv
import time
from dataclasses import dataclass
from pathlib import Path

from backend.api.schemas import CheckRequest
from backend.config.settings import Settings
from backend.evaluation.metrics import ClassificationMetrics, compute_classification_metrics
from backend.services.hallucination_service import HallucinationService

_REQUIRED_COLUMNS = {"question", "answer", "label"}


@dataclass(frozen=True, slots=True)
class DatasetRow:
    """One labeled question/answer pair to assess."""

    question: str
    answer: str
    label: bool
    context: list[str]


@dataclass(frozen=True, slots=True)
class DatasetEvaluationReport:
    """Aggregate benchmark results for a labeled dataset run."""

    sample_count: int
    metrics: ClassificationMetrics
    mean_latency_ms: float
    p95_latency_ms: float


def load_dataset(dataset_path: Path) -> list[DatasetRow]:
    """Load labeled rows from a CSV with question, answer, label, and optional context.

    ``label`` uses the same convention as classifier training data: 0 for an
    evidence-supported answer, 1 for a hallucination. ``context`` is optional
    and pipe-separated when multiple trusted passages apply to one row.
    """
    with dataset_path.open(encoding="utf-8", newline="") as file:
        reader = csv.DictReader(file)
        missing_columns = _REQUIRED_COLUMNS - set(reader.fieldnames or [])
        if missing_columns:
            raise ValueError(f"Dataset is missing required columns: {sorted(missing_columns)}")
        rows = [
            DatasetRow(
                question=row["question"],
                answer=row["answer"],
                label=bool(int(row["label"])),
                context=[part for part in row.get("context", "").split("|") if part],
            )
            for row in reader
        ]
    if not rows:
        raise ValueError("Dataset must contain at least one labelled row")
    return rows


def run_dataset_evaluation(dataset_path: Path, settings: Settings) -> DatasetEvaluationReport:
    """Score every row with the configured detection pipeline and summarize results."""
    rows = load_dataset(dataset_path)
    service = HallucinationService(settings)
    labels: list[bool] = []
    predictions: list[bool] = []
    latencies_ms: list[float] = []
    for row in rows:
        request = CheckRequest(question=row.question, answer=row.answer, context=row.context)
        started_at = time.perf_counter()
        response = service.assess(request, persist=False)
        latencies_ms.append((time.perf_counter() - started_at) * 1000)
        labels.append(row.label)
        predictions.append(response.hallucination)

    latencies_ms.sort()
    p95_index = max(0, int(len(latencies_ms) * 0.95) - 1)
    return DatasetEvaluationReport(
        sample_count=len(rows),
        metrics=compute_classification_metrics(labels, predictions),
        mean_latency_ms=round(sum(latencies_ms) / len(latencies_ms), 3),
        p95_latency_ms=round(latencies_ms[p95_index], 3),
    )

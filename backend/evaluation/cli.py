"""Command-line entry point for offline dataset benchmarking."""

import argparse
import json
from pathlib import Path

from backend.config.settings import get_settings
from backend.evaluation.dataset_runner import run_dataset_evaluation


def main() -> None:
    """Run the detection pipeline over a labeled CSV and print a metrics report."""
    parser = argparse.ArgumentParser(
        description="Benchmark the hallucination detector against a labeled dataset."
    )
    parser.add_argument(
        "dataset", type=Path, help="CSV file with question, answer, label[, context] columns."
    )
    parser.add_argument(
        "--json", action="store_true", help="Print the report as JSON instead of a table."
    )
    args = parser.parse_args()

    report = run_dataset_evaluation(args.dataset, get_settings())
    if args.json:
        print(
            json.dumps(
                {
                    "sample_count": report.sample_count,
                    "accuracy": report.metrics.accuracy,
                    "precision": report.metrics.precision,
                    "recall": report.metrics.recall,
                    "f1": report.metrics.f1,
                    "mean_latency_ms": report.mean_latency_ms,
                    "p95_latency_ms": report.p95_latency_ms,
                },
                indent=2,
            )
        )
        return

    print(f"Samples:       {report.sample_count}")
    print(f"Accuracy:      {report.metrics.accuracy:.2%}")
    print(f"Precision:     {report.metrics.precision:.2%}")
    print(f"Recall:        {report.metrics.recall:.2%}")
    print(f"F1:            {report.metrics.f1:.2%}")
    print(f"Mean latency:  {report.mean_latency_ms:.2f} ms")
    print(f"P95 latency:   {report.p95_latency_ms:.2f} ms")


if __name__ == "__main__":
    main()

# Offline dataset benchmarking

The benchmark harness scores a labeled dataset with the full detection pipeline
and reports classification metrics and latency. It requires no database and
never persists results, so runs are reproducible.

Prepare a UTF-8 CSV with `question`, `answer`, and `label` columns. An optional
`context` column supplies pipe-separated trusted passages for a row:

```csv
question,answer,label,context
What is the capital of France?,Paris is the capital of France.,0,Paris is the capital of France.
What is the capital of France?,Lyon is the capital of France.,1,
```

`label=0` denotes an evidence-supported answer and `label=1` denotes a
hallucinated or unsupported answer, matching the classifier training convention.

Run the benchmark:

```bash
python -m backend.evaluation.cli experiments/sample_dataset.csv
```

```text
Samples:       10
Accuracy:      80.00%
Precision:     100.00%
Recall:        60.00%
F1:            75.00%
Mean latency:  0.13 ms
P95 latency:   0.12 ms
```

These numbers are the transparent baseline, not a target. Synonym-aware matching,
safe-word filtering, and a technical-token mismatch signal raised recall from an
earlier 40% (named-entity and numeric signals only) to 60% while holding
precision at 100%. The two remaining misses in the sample set are semantic
contradictions with no lexical novelty—a single named-entity substitution in an
otherwise supported sentence, and an antonym/domain-term swap. Closing that gap
is the goal of the embedding-similarity and fine-tuned classifier phases, which
this benchmark measures against the fixed lexical baseline.

Add `--json` for machine-readable output suitable for CI dashboards or paper
tables. Evaluate every model on the same held-out split and retain dataset
versions for reproducibility.

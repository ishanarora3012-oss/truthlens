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
Accuracy:      70.00%
Precision:     100.00%
Recall:        40.00%
F1:            57.14%
Mean latency:  0.11 ms
P95 latency:   0.10 ms
```

These numbers are the transparent baseline, not a target. High precision with
lower recall is expected: the baseline flags named-entity and numeric mismatches
confidently but misses hallucinations that are lexically close to the evidence
(for example `CO2` versus `H2O`). The benchmark exists to quantify that gap and
to measure the synonym-aware matching and fine-tuned classifier phases against a
fixed baseline.

Add `--json` for machine-readable output suitable for CI dashboards or paper
tables. Evaluate every model on the same held-out split and retain dataset
versions for reproducibility.

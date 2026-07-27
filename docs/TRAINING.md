# Training a transformer classifier

The default API uses the transparent evidence-grounded baseline. Fine-tuned
classifiers are optional so local development and API startup never download
model weights automatically.

Prepare a UTF-8 CSV with exactly these columns:

```csv
question,answer,label
What is the capital of France?,Paris is the capital of France.,0
What is the capital of France?,Lyon is the capital of France.,1
```

`label=0` denotes an evidence-supported answer and `label=1` denotes a
hallucinated or unsupported answer. Train one family explicitly:

```python
from backend.models.deberta.train import train

result = train("data/processed/train.csv", "artifacts/deberta")
print(result)
```

The trainer saves HuggingFace model and tokenizer artifacts in the output
directory. Use the corresponding `predict` function with that directory to
obtain a class-1 hallucination probability. Evaluate all models on the same
held-out split, report confidence intervals, and retain dataset/model versions
for reproducibility.

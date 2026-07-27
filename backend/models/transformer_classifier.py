"""Reusable fine-tuning and inference utilities for transformer classifiers.

Imports of PyTorch and Transformers are intentionally deferred so the API can
run the transparent baseline without loading model libraries or checkpoints.
"""

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True, slots=True)
class TransformerTrainingConfig:
    """Configuration for a binary hallucination-classifier fine-tuning run."""

    model_name: str
    dataset_path: Path
    output_dir: Path
    epochs: int = 3
    batch_size: int = 8
    learning_rate: float = 2e-5
    max_length: int = 256


@dataclass(frozen=True, slots=True)
class TrainingResult:
    """Versioned artifact metadata returned after a training run."""

    model_name: str
    output_dir: Path
    examples_seen: int


def _load_rows(dataset_path: Path) -> list[dict[str, object]]:
    """Load CSV training rows with question, answer, and binary label columns."""
    import pandas as pd

    frame = pd.read_csv(dataset_path)
    required_columns = {"question", "answer", "label"}
    missing_columns = required_columns - set(frame.columns)
    if missing_columns:
        raise ValueError(f"Dataset is missing required columns: {sorted(missing_columns)}")
    if frame.empty:
        raise ValueError("Dataset must contain at least one labelled example")
    labels = set(frame["label"].dropna().astype(int).unique())
    if not labels <= {0, 1}:
        raise ValueError("label must use binary values 0 (supported) or 1 (hallucination)")
    return frame.loc[:, ["question", "answer", "label"]].to_dict(orient="records")


def train_classifier(config: TransformerTrainingConfig) -> TrainingResult:
    """Fine-tune a HuggingFace sequence classifier from a labelled CSV dataset."""
    import torch
    from torch.optim import AdamW
    from torch.utils.data import DataLoader, Dataset
    from transformers import AutoModelForSequenceClassification, AutoTokenizer

    rows = _load_rows(config.dataset_path)
    tokenizer = AutoTokenizer.from_pretrained(config.model_name)
    model = AutoModelForSequenceClassification.from_pretrained(config.model_name, num_labels=2)

    class HallucinationDataset(Dataset[dict[str, torch.Tensor]]):
        def __len__(self) -> int:
            return len(rows)

        def __getitem__(self, index: int) -> dict[str, torch.Tensor]:
            row = rows[index]
            encoded = tokenizer(
                str(row["question"]),
                str(row["answer"]),
                truncation=True,
                max_length=config.max_length,
                padding="max_length",
                return_tensors="pt",
            )
            return {
                "input_ids": encoded["input_ids"].squeeze(0),
                "attention_mask": encoded["attention_mask"].squeeze(0),
                "labels": torch.tensor(int(row["label"]), dtype=torch.long),
            }

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model.to(device)
    model.train()
    optimizer = AdamW(model.parameters(), lr=config.learning_rate)
    loader = DataLoader(HallucinationDataset(), batch_size=config.batch_size, shuffle=True)
    for _ in range(config.epochs):
        for batch in loader:
            optimizer.zero_grad()
            output = model(**{key: value.to(device) for key, value in batch.items()})
            if output.loss is None:
                raise RuntimeError("Transformer model did not return a training loss")
            output.loss.backward()
            optimizer.step()
    config.output_dir.mkdir(parents=True, exist_ok=True)
    model.save_pretrained(config.output_dir)
    tokenizer.save_pretrained(config.output_dir)
    return TrainingResult(config.model_name, config.output_dir, len(rows))


def predict_probability(
    question: str, answer: str, checkpoint_dir: Path, max_length: int = 256
) -> float:
    """Return the hallucination probability from a saved binary classifier."""
    import torch
    from transformers import AutoModelForSequenceClassification, AutoTokenizer

    if not checkpoint_dir.exists():
        raise FileNotFoundError(f"Checkpoint does not exist: {checkpoint_dir}")
    tokenizer = AutoTokenizer.from_pretrained(checkpoint_dir)
    model = AutoModelForSequenceClassification.from_pretrained(checkpoint_dir)
    model.eval()
    encoded = tokenizer(
        question, answer, truncation=True, max_length=max_length, return_tensors="pt"
    )
    with torch.inference_mode():
        logits = model(**encoded).logits
    return round(float(torch.softmax(logits, dim=-1)[0, 1]), 6)

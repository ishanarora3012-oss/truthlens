# TRUTHLENS project summary

TRUTHLENS is an evidence-grounded framework for evaluating whether an LLM answer
introduces claims not supported by trusted context. It is designed as a research
baseline and application platform—not as a guarantee of factual correctness.

## What is implemented

- FastAPI API with typed OpenAPI contracts.
- Local curated knowledge-base retrieval plus caller-provided trusted context.
- Transparent baseline scoring based on lexical semantic similarity, answer
  coverage, curated synonym-aware matching, safe-word filtering, and
  numeric-, named-entity-, and technical-token mismatch signals.
- An offline, database-free benchmark CLI that scores a labeled dataset and
  reports accuracy, precision, recall, F1, and latency.
- Calibrated, bounded confidence and explicit "insufficient evidence" behavior.
- Token-support explanation compatible with future LIME/SHAP/attention adapters.
- SQLite-by-default history persistence; PostgreSQL is supported through Docker.
- A benchmark endpoint that evaluates multiple named model responses under an
  identical question and context.
- React dashboard for submitting assessments and inspecting evidence.
- Docker, GitHub Actions, static quality configuration, and unit tests.

## Research interpretation

The primary score is an **unsupported-claim risk score**, not an absolute truth
score. A high score indicates that retrieved evidence does not support material
answer content. A low score indicates support only relative to the evidence
available to the system. When no relevant evidence is found, TRUTHLENS returns
low confidence rather than declaring an answer factual.

## Extension points

- Replace `EvidenceRetriever` with a vector store, enterprise search, or web
  retrieval provider that preserves provenance.
- Replace curated synonyms with Sentence Transformer embedding similarity for
  open-domain paraphrase and contradiction detection.
- Replace `EvidenceGroundedAssessmentEngine` with a calibrated fine-tuned BERT,
  RoBERTa, DeBERTa, or DistilBERT classifier.
- Attach SHAP/LIME explanations to a selected trained model.
- Add provider adapters for GPT, Llama, Gemma, Mistral, DeepSeek, and Phi.
- Add dataset versioning, model registry, Alembic migrations, authentication,
  tracing, rate limits, and human-review workflows before high-scale deployment.

## Safety and limitations

TRUTHLENS should not be used as the sole decision-maker in medical, legal,
financial, or other high-stakes settings. Retrieval quality, corpus coverage,
and prompt/domain shift all affect outcomes. Keep the evidence shown to users,
measure performance on a labelled in-domain set, and route uncertain outcomes
to human review.

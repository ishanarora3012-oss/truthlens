# TRUTHLENS

**TRUTHLENS** is a production-oriented research framework for detecting and
benchmarking hallucinations in Large Language Model (LLM) outputs. It is
designed to combine evidence retrieval, semantic similarity, classifier-based
assessment, calibrated confidence, and explainability in one reproducible
system.

> Status: runnable research baseline. TRUTHLENS provides transparent,
> evidence-grounded unsupported-claim detection and clear extension points for
> trained classifiers and production retrieval.

## Architecture

```text
Question + LLM Answer
        │
        ▼
Evidence Retrieval → Semantic Similarity → Unsupported-claim Classifier
        │                                           │
        └────────── Confidence Estimation ←─────────┘
                              │
                              ▼
                    Explainability (SHAP / LIME / attention)
                              │
                              ▼
                       REST API and React dashboard
```

The backend uses Clean Architecture-inspired boundaries: API routes own HTTP
contracts, services orchestrate use cases, repositories isolate persistence,
and retrieval, scoring, explainability, and evaluation remain independently
testable. The default engine uses transparent token-support features rather
than downloading a model at startup.

Read the detailed [project summary](docs/PROJECT_SUMMARY.md) and
[API reference](docs/API.md) before evaluating research results. For optional
fine-tuning of BERT, RoBERTa, DeBERTa, or DistilBERT, see the
[training guide](docs/TRAINING.md).

## Installation

Prerequisites: Python 3.12+, Node.js 22+, and Docker (optional).

```bash
git clone <your-repository-url>
cd truthlens
python3.12 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn backend.main:app --reload
```

The API is served at `http://localhost:8000`; interactive OpenAPI docs are at
`http://localhost:8000/docs`.

For the containerized API, dashboard, and PostgreSQL stack:

```bash
docker compose up --build
```

The dashboard is then available at `http://localhost:5173`.

The dashboard scaffold can be started separately:

```bash
cd frontend
npm install
npm run dev
```

## API documentation

### `GET /api/v1/health`

Returns API liveness.

```json
{"status":"ok"}
```

### `POST /api/v1/check`

Assesses an answer against optional trusted context and local curated evidence.
It returns an unsupported-claim risk score, confidence, evidence provenance,
and a token-level explanation. It intentionally returns low confidence when no
relevant evidence is available.

```json
{
  "question": "What is the capital of France?",
  "answer": "Paris is the capital of France."
}
```

Response shape:

```json
{
  "hallucination": false,
  "hallucination_score": 0.12,
  "confidence": 91.0,
  "reason": "The answer is substantially supported by retrieved evidence.",
  "evidence": [],
  "explanation": {"method": "evidence-grounded token attribution (LIME-compatible schema)"}
}
```

### Additional endpoints

- `GET /api/v1/history?limit=20` returns persisted recent assessments.
- `POST /api/v1/benchmark` evaluates a mapping of model names to answers under
  one identical question and context.

## Folder structure

```text
truthlens/
├── backend/
│   ├── api/             # FastAPI routes and schemas
│   ├── config/          # Environment-backed settings
│   ├── database/        # SQLAlchemy foundation and entities
│   ├── evaluation/      # Benchmarking and metrics
│   ├── explainability/  # SHAP, LIME, and attention adapters
│   ├── models/          # BERT, RoBERTa, DeBERTa, DistilBERT adapters
│   └── services/        # Pipeline orchestration contracts
├── frontend/            # React + TypeScript + Tailwind dashboard scaffold
├── data/                # Git-ignored raw and processed datasets
├── docs/ experiments/ notebooks/
├── tests/
└── .github/workflows/   # Continuous integration
```

## Method and limitations

The included detector is a reproducible baseline for **evidence support**, not
an absolute truth oracle. Scores depend on retrieval quality and coverage. A
low score means the available evidence supports the answer; it does not prove
the answer correct. Review the [limitations and safety guidance](docs/PROJECT_SUMMARY.md#safety-and-limitations)
before use in high-stakes domains.

## Future work

- Add vector/web retrieval and provenance persistence.
- Add Sentence Transformer similarity and calibrated classifier inference.
- Fine-tune and compare BERT, RoBERTa, DeBERTa, and DistilBERT.
- Add SHAP, LIME, and attention explanations.
- Build dashboard assessments, model comparisons, charts, and history.
- Benchmark GPT, Llama, Gemma, Mistral, DeepSeek, and Phi on identical prompts.
- Add Alembic migrations, authentication, observability, and deployment hardening.

## License

This project is licensed under the [MIT License](LICENSE).

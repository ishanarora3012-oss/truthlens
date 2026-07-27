# TRUTHLENS

**TRUTHLENS** is a production-oriented research framework for detecting and
benchmarking hallucinations in Large Language Model (LLM) outputs. It is
designed to combine evidence retrieval, semantic similarity, classifier-based
assessment, calibrated confidence, and explainability in one reproducible
system.

> Status: project scaffold. The API contract and component boundaries are in
> place; detection, retrieval, and benchmarking logic are intentionally not yet
> implemented.

## Architecture

```text
Question + LLM Answer
        │
        ▼
Evidence Retrieval → Semantic Similarity → Hallucination Classifier
        │                                           │
        └────────── Confidence Estimation ←─────────┘
                              │
                              ▼
                    Explainability (SHAP / LIME / attention)
                              │
                              ▼
                       REST API and React dashboard
```

The backend uses Clean Architecture-inspired boundaries: the API layer owns
HTTP contracts, services orchestrate use cases, model adapters own inference,
and evaluation/explainability modules remain independently testable.

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

For the containerized API and PostgreSQL stack:

```bash
docker compose up --build
```

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

Reserves the Phase 1 assessment contract. It currently returns `501 Not
Implemented` until the pipeline is added.

```json
{
  "question": "What is the capital of France?",
  "answer": "Paris is the capital of France."
}
```

Target response contract:

```json
{
  "hallucination": true,
  "confidence": 95.3,
  "reason": "Named entity mismatch"
}
```

## Folder structure

```text
truthlens/
├── backend/
│   ├── api/             # FastAPI routes and schemas
│   ├── config/          # Environment-backed settings
│   ├── database/        # SQLAlchemy foundation and entities
│   ├── evaluation/      # Benchmarking and metrics
│   ├── explainability/  # SHAP, LIME, and attention adapters
│   ├── models/          # BERT, RoBERTa, DeBERTa, DistilBERT placeholders
│   └── services/        # Pipeline orchestration contracts
├── frontend/            # React + TypeScript + Tailwind dashboard scaffold
├── data/                # Git-ignored raw and processed datasets
├── docs/ experiments/ notebooks/
├── tests/
└── .github/workflows/   # Continuous integration
```

## Future work

- Implement evidence retrieval and provenance persistence.
- Add Sentence Transformer similarity and calibrated classifier inference.
- Fine-tune and compare BERT, RoBERTa, DeBERTa, and DistilBERT.
- Add SHAP, LIME, and attention explanations.
- Build dashboard assessments, model comparisons, charts, and history.
- Benchmark GPT, Llama, Gemma, Mistral, DeepSeek, and Phi on identical prompts.
- Add Alembic migrations, authentication, observability, and deployment hardening.

## License

This project is licensed under the [MIT License](LICENSE).

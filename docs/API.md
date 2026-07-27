# API reference

All endpoints are prefixed with `/api/v1`. Interactive OpenAPI documentation is
available at `/docs` while the service is running.

## `POST /check`

Evaluates one answer against optional caller context and the local knowledge base.

```json
{
  "question": "What is the capital of France?",
  "answer": "Paris is the capital of France.",
  "context": ["Paris is the capital and most populous city of France."]
}
```

The result includes `hallucination`, an unsupported-claim `hallucination_score`
from 0 to 1, confidence from 0 to 100, retrieved evidence, and token support.

## `GET /history?limit=20`

Returns recently persisted assessments, newest first. `limit` accepts 1–100.

## `POST /benchmark`

Assesses named model outputs under the same question and trusted context. It
does not call model providers; callers supply outputs to ensure reproducibility.

```json
{
  "question": "What is the capital of France?",
  "context": ["Paris is the capital and most populous city of France."],
  "responses": {
    "GPT": "Paris is France's capital.",
    "Example model": "Lyon is the capital of France."
  }
}
```

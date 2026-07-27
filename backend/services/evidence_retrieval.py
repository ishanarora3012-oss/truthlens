"""Local knowledge-base and caller-context evidence retrieval."""

import json
import re
from dataclasses import dataclass
from pathlib import Path

_TOKEN_PATTERN = re.compile(r"[a-zA-Z0-9]+")


@dataclass(frozen=True, slots=True)
class EvidenceDocument:
    """A normalized, provenance-bearing evidence document."""

    id: str
    title: str
    content: str
    source: str | None
    relevance: float


def _tokens(value: str) -> set[str]:
    return {token.lower() for token in _TOKEN_PATTERN.findall(value) if len(token) > 2}


class EvidenceRetriever:
    """Retrieve evidence from trusted caller context and a local curated corpus.

    The interface is deliberately provider-neutral: a web, vector, or enterprise
    retriever can replace this implementation without changing assessment code.
    """

    def __init__(self, knowledge_base_path: str) -> None:
        self._knowledge_base_path = Path(knowledge_base_path)

    def _load_documents(self) -> list[dict[str, str]]:
        if not self._knowledge_base_path.exists():
            return []
        with self._knowledge_base_path.open(encoding="utf-8") as file:
            return json.load(file)

    def retrieve(
        self, question: str, answer: str, context: list[str] | None = None
    ) -> list[EvidenceDocument]:
        """Rank up to five evidence passages by lexical overlap.

        Caller-provided context is considered authoritative for the assessment and
        is always included before local corpus candidates.
        """
        query_tokens = _tokens(f"{question} {answer}")
        evidence: list[EvidenceDocument] = []
        for index, passage in enumerate(context or []):
            evidence.append(
                EvidenceDocument(
                    id=f"provided-{index + 1}",
                    title="Caller-provided context",
                    content=passage,
                    source=None,
                    relevance=1.0,
                )
            )

        candidates: list[EvidenceDocument] = []
        for document in self._load_documents():
            content = document["content"]
            document_tokens = _tokens(f"{document['title']} {content}")
            union = query_tokens | document_tokens
            relevance = len(query_tokens & document_tokens) / len(union) if union else 0.0
            if relevance > 0:
                candidates.append(
                    EvidenceDocument(
                        id=document["id"],
                        title=document["title"],
                        content=content,
                        source=document.get("source"),
                        relevance=round(relevance, 4),
                    )
                )
        candidates.sort(key=lambda item: item.relevance, reverse=True)
        return (evidence + candidates)[:5]

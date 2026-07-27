"""Curated synonym and safe-word resources for the baseline detector.

These are deliberately dependency-free. A curated synonym map keeps the baseline
transparent and fast; embedding-based similarity (Sentence Transformers) is the
documented extension point for open-domain coverage.
"""

import json
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path


@dataclass(frozen=True, slots=True)
class LexicalResources:
    """Synonym expansion and safe-word filtering for token support checks."""

    synonyms: dict[str, frozenset[str]]
    safe_words: frozenset[str]

    def is_safe(self, token: str) -> bool:
        """Return whether a token is a generic term excluded from scoring."""
        return token in self.safe_words

    def expand(self, token: str) -> frozenset[str]:
        """Return the token together with its curated synonyms."""
        return self.synonyms.get(token, frozenset({token}))

    def is_supported(self, token: str, evidence_tokens: frozenset[str]) -> bool:
        """Return whether a token or any of its synonyms appears in the evidence."""
        return bool(self.expand(token) & evidence_tokens)


def _load_synonyms(path: Path) -> dict[str, frozenset[str]]:
    if not path.exists():
        return {}
    payload = json.loads(path.read_text(encoding="utf-8"))
    mapping: dict[str, frozenset[str]] = {}
    for group in payload.get("groups", []):
        members = frozenset(term.lower() for term in group)
        for term in members:
            mapping[term] = members
    return mapping


def _load_safe_words(path: Path) -> frozenset[str]:
    if not path.exists():
        return frozenset()
    lines = path.read_text(encoding="utf-8").splitlines()
    return frozenset(
        line.strip().lower()
        for line in lines
        if line.strip() and not line.startswith("#")
    )


@lru_cache(maxsize=8)
def load_lexical_resources(synonyms_path: str, safe_words_path: str) -> LexicalResources:
    """Load and cache synonym and safe-word resources by file path."""
    return LexicalResources(
        synonyms=_load_synonyms(Path(synonyms_path)),
        safe_words=_load_safe_words(Path(safe_words_path)),
    )

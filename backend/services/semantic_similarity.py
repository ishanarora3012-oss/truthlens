"""Deterministic semantic similarity features for the baseline detector."""

import math
import re
from collections import Counter

_TOKEN_PATTERN = re.compile(r"[a-zA-Z0-9]+")
_STOP_WORDS = {
    "a",
    "an",
    "and",
    "are",
    "as",
    "at",
    "be",
    "by",
    "for",
    "from",
    "in",
    "is",
    "it",
    "of",
    "on",
    "or",
    "that",
    "the",
    "to",
    "was",
    "were",
    "with",
}


def tokenize(text: str) -> list[str]:
    """Normalize meaningful tokens for transparent baseline features."""
    return [
        token.lower()
        for token in _TOKEN_PATTERN.findall(text)
        if len(token) > 1 and token.lower() not in _STOP_WORDS
    ]


def cosine_similarity(left: str, right: str) -> float:
    """Return cosine similarity between token-frequency vectors."""
    left_counts, right_counts = Counter(tokenize(left)), Counter(tokenize(right))
    if not left_counts or not right_counts:
        return 0.0
    numerator = sum(left_counts[token] * right_counts[token] for token in left_counts)
    left_norm = math.sqrt(sum(value * value for value in left_counts.values()))
    right_norm = math.sqrt(sum(value * value for value in right_counts.values()))
    return round(numerator / (left_norm * right_norm), 4)

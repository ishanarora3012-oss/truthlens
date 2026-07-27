"""Tests for curated synonym and safe-word resources."""

from backend.services.lexical_resources import LexicalResources, load_lexical_resources


def test_synonyms_match_symmetrically() -> None:
    """A curated synonym should be recognized in either direction."""
    resources = load_lexical_resources("data/synonyms.json", "data/safe_words.txt")

    assert resources.is_supported("car", frozenset({"automobile"}))
    assert resources.is_supported("automobile", frozenset({"car"}))
    assert not resources.is_supported("car", frozenset({"bicycle"}))


def test_safe_words_are_excluded() -> None:
    """Generic terms load from the safe-word list and are flagged as safe."""
    resources = load_lexical_resources("data/synonyms.json", "data/safe_words.txt")

    assert resources.is_safe("thing")
    assert not resources.is_safe("paris")


def test_expand_falls_back_to_the_token_itself() -> None:
    """A token without curated synonyms expands to just itself."""
    resources = LexicalResources(synonyms={}, safe_words=frozenset())

    assert resources.expand("quantum") == frozenset({"quantum"})

"""Evidence retrieval service contract."""


class EvidenceRetriever:
    """Retrieve authoritative evidence for an input question and answer."""

    def retrieve(self, question: str, answer: str) -> list[str]:
        """Return evidence passages.

        TODO: implement provider-agnostic retrieval, ranking, provenance, and caching.
        """
        raise NotImplementedError

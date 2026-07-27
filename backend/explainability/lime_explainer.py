"""Local explanation adapter with a transparent baseline implementation."""

from backend.api.schemas import Explanation
from backend.explainability.attention import extract_attention


class LimeExplainer:
    """Produce a stable token-support explanation compatible with LIME output."""

    def explain(self, supported: list[str], unsupported: list[str], reason: str) -> Explanation:
        """Build an explanation safe for API and dashboard consumption."""
        return Explanation(
            summary=reason,
            supported_claims=list(dict.fromkeys(supported))[:10],
            unsupported_claims=list(dict.fromkeys(unsupported))[:10],
            token_attributions=extract_attention(supported, unsupported),
            method="evidence-grounded token attribution (LIME-compatible schema)",
        )

"""Token-support visualization for models without exposed attention tensors."""

from backend.api.schemas import TokenAttribution


def extract_attention(supported: list[str], unsupported: list[str]) -> list[TokenAttribution]:
    """Create normalized token-support attributions for dashboard highlighting."""
    attributions = [
        TokenAttribution(token=token, contribution=0.65, label="supported")
        for token in dict.fromkeys(supported)
    ]
    attributions.extend(
        TokenAttribution(token=token, contribution=-0.75, label="unsupported")
        for token in dict.fromkeys(unsupported)
    )
    return attributions[:24]

"""SHAP adapter boundary for trained classifier integrations."""


class ShapExplainer:
    """Lazy boundary for model-specific SHAP explanations."""

    def explain(self) -> None:
        """Reserve the trained-model SHAP integration point."""
        raise RuntimeError("SHAP explanations require a configured trained classifier.")

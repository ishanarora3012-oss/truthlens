"""Provider-agnostic multi-LLM benchmark data structures."""

from collections.abc import Callable

from backend.api.schemas import BenchmarkResponse, BenchmarkResult, CheckRequest
from backend.services.hallucination_service import HallucinationService


class BenchmarkRunner:
    """Run identical prompt sets against configured answer providers.

    Providers are callables so integrations for GPT, Llama, Gemma, Mistral,
    DeepSeek, and Phi can live outside the core evaluation package.
    """

    def __init__(self, assess: HallucinationService) -> None:
        self._assess = assess

    def run(
        self,
        question: str,
        providers: dict[str, Callable[[str], str]],
        context: list[str] | None = None,
    ) -> BenchmarkResponse:
        """Generate and assess one answer per named model provider."""
        results = [
            BenchmarkResult(
                model=name,
                assessment=self._assess.assess(
                    CheckRequest(
                        question=question, answer=provider(question), context=context or []
                    ),
                    persist=False,
                ),
            )
            for name, provider in providers.items()
        ]
        return BenchmarkResponse(question=question, results=results)

"""Logging configuration helpers."""

import logging


def configure_logging(level: str) -> None:
    """Configure process-wide structured-friendly logging defaults."""
    logging.basicConfig(
        level=level.upper(),
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    )

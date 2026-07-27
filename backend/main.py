"""FastAPI application factory and entry point."""

from contextlib import asynccontextmanager
from typing import AsyncIterator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.api.router import api_router
from backend.config.settings import get_settings
from backend.utils.logging import configure_logging

settings = get_settings()


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    """Initialize and release application-owned resources."""
    configure_logging(settings.log_level)
    # TODO: initialize database connections and model registry.
    yield
    # TODO: release database connections and model resources.


app = FastAPI(
    title=settings.app_name,
    description="Multi-LLM hallucination detection and benchmarking framework.",
    version="0.1.0",
    lifespan=lifespan,
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(api_router, prefix=settings.api_v1_prefix)

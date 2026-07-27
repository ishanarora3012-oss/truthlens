"""Root API router composition."""

from fastapi import APIRouter

from backend.api.routes import benchmark, check, health, history

api_router = APIRouter()
api_router.include_router(health.router)
api_router.include_router(check.router)
api_router.include_router(history.router)
api_router.include_router(benchmark.router)

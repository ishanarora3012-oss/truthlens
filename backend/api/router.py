"""Root API router composition."""

from fastapi import APIRouter

from backend.api.routes import check, health

api_router = APIRouter()
api_router.include_router(health.router)
api_router.include_router(check.router)

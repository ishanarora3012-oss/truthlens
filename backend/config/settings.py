"""Typed application settings loaded from the environment."""

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Runtime settings for the TRUTHLENS API."""

    app_name: str = "TRUTHLENS"
    environment: str = "development"
    debug: bool = False
    api_v1_prefix: str = "/api/v1"
    database_url: str = "postgresql+psycopg://truthlens:truthlens@localhost:5432/truthlens"
    cors_origins: str = "http://localhost:5173"
    log_level: str = "INFO"
    hallucination_threshold: float = 0.60
    knowledge_base_path: str = "data/knowledge_base.json"

    model_config = SettingsConfigDict(env_file=".env", env_prefix="TRUTHLENS_", extra="ignore")

    @property
    def cors_origin_list(self) -> list[str]:
        """Return normalized CORS origins."""
        return [origin.strip() for origin in self.cors_origins.split(",") if origin.strip()]


@lru_cache
def get_settings() -> Settings:
    """Return cached application settings."""
    return Settings()

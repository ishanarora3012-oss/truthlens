"""Database engine and session factory placeholders."""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from backend.config.settings import get_settings

settings = get_settings()

# TODO: configure pooling, migrations, and lifecycle-aware dependency injection.
engine = create_engine(settings.database_url, pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

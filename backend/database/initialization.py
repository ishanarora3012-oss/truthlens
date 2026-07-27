"""Schema initialization for local and container deployments."""

from backend.database import models  # noqa: F401 - registers SQLAlchemy mappings
from backend.database.base import Base
from backend.database.session import engine


def initialize_database() -> None:
    """Create initial tables when migrations are not yet configured.

    Alembic should replace this bootstrap operation before a multi-instance
    production deployment.
    """
    Base.metadata.create_all(bind=engine)

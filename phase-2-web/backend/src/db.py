"""
Database connection and session management.

Uses SQLModel with PostgreSQL via Neon.
"""
from typing import Generator
from sqlmodel import create_engine, Session, SQLModel
from .config import settings


engine = create_engine(
    settings.database_url,
    echo=True,  # Enable SQL logging for development
)


def init_db() -> None:
    """Create all database tables if they don't exist."""
    SQLModel.metadata.create_all(engine)


def get_session() -> Generator[Session, None, None]:
    """
    Dependency for FastAPI routes.

    Yields a database session and ensures it's closed after use.
    """
    with Session(engine) as session:
        yield session

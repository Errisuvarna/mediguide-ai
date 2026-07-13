"""
SQLAlchemy engine / session setup.

Uses SQLite by default (file-based, zero external services required —
ideal for a hackathon build). Swap DATABASE_URL to a Postgres DSN in
.env and this module needs no other changes, since SQLAlchemy
abstracts the dialect.
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from app.config import settings

connect_args = {"check_same_thread": False} if settings.DATABASE_URL.startswith("sqlite") else {}

engine = create_engine(settings.DATABASE_URL, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db() -> None:
    """Create all tables. Called on app startup."""
    from app import models  # noqa: F401  (ensure models are registered)
    Base.metadata.create_all(bind=engine)

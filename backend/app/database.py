"""Engine and session factory. Creating an engine opens no connection (ASG-FR-032 needs
the app to start, and to answer 503 on /ready, while PostgreSQL is still down)."""

from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session, sessionmaker


def create_db_engine(url: str, connect_timeout_seconds: float = 1.0) -> Engine:
    return create_engine(
        url,
        pool_pre_ping=True,
        connect_args={
            "connect_timeout": max(1, round(connect_timeout_seconds)),
            "options": "-c timezone=UTC",  # timestamptz values come back in UTC
        },
    )


def create_session_factory(engine: Engine) -> sessionmaker[Session]:
    return sessionmaker(engine, expire_on_commit=False)

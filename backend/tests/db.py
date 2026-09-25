"""Helpers and fixtures for the tests that need a real PostgreSQL 16 (TEST_DATABASE_URL).

Locally: any PostgreSQL 16 database that may be wiped, for example
``TEST_DATABASE_URL=postgresql+psycopg://postgres@127.0.0.1:5433/civicpulse_test``.
In CI it is the service container. The tests drop and recreate the ``public`` schema.
"""

import os
import uuid
from collections.abc import Iterator
from pathlib import Path

import pytest
from alembic import command
from alembic.config import Config
from sqlalchemy import Engine, text
from sqlalchemy.orm import Session

from app.database import create_db_engine
from app.domain import Category, Priority
from app.repositories.complaints import NewComplaint

BACKEND = Path(__file__).resolve().parent.parent


def alembic_config(url: str) -> Config:
    config = Config(str(BACKEND / "alembic.ini"))
    config.set_main_option("script_location", str(BACKEND / "alembic"))
    config.set_main_option("sqlalchemy.url", url)
    return config


def reset_schema(engine: Engine) -> None:
    with engine.begin() as connection:
        connection.execute(text("DROP SCHEMA IF EXISTS public CASCADE"))
        connection.execute(text("CREATE SCHEMA public"))


def new_complaint(**overrides: object) -> NewComplaint:
    values: dict[str, object] = {
        "text": "Water has not reached our street for three days.",
        "location": "Street 5, Model Town",
        "reporter_contact": None,
        "category": Category.WATER,
        "priority": Priority.HIGH,
        "ai_summary": "No water for three days",
        "triaged_by": "rules",
        "triage_latency_ms": 12,
    }
    values.update(overrides)
    return NewComplaint(**values)  # type: ignore[arg-type]


@pytest.fixture(scope="session")
def db_url() -> str:
    url = os.environ.get("TEST_DATABASE_URL")
    if not url:
        pytest.skip("TEST_DATABASE_URL is not set: these tests need PostgreSQL 16")
    return url


@pytest.fixture(scope="session")
def engine(db_url: str) -> Iterator[Engine]:
    db_engine = create_db_engine(db_url, 5)
    yield db_engine
    db_engine.dispose()


@pytest.fixture(scope="session")
def migrated(engine: Engine, db_url: str) -> Engine:
    reset_schema(engine)
    command.upgrade(alembic_config(db_url), "head")
    return engine


@pytest.fixture
def session(migrated: Engine) -> Iterator[Session]:
    """A session whose work is rolled back at the end of the test."""
    connection = migrated.connect()
    transaction = connection.begin()
    db_session = Session(bind=connection, join_transaction_mode="create_savepoint")
    yield db_session
    db_session.close()
    transaction.rollback()
    connection.close()


def fresh_id() -> uuid.UUID:
    return uuid.uuid4()

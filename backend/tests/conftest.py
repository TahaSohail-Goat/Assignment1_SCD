import threading
from collections.abc import Iterator

import pytest

from app.config import Settings
from tests.db import db_url, engine, migrated, session  # noqa: F401  (database fixtures)


class FakeProbe:
    """A dependency probe that succeeds, fails, or blocks until the test releases it."""

    def __init__(
        self, name: str, error: Exception | None = None, block: threading.Event | None = None
    ) -> None:
        self.name = name
        self.error = error
        self.block = block
        self.calls = 0

    def check(self) -> None:
        self.calls += 1
        if self.block is not None:
            self.block.wait(timeout=10)
        if self.error is not None:
            raise self.error


@pytest.fixture
def settings() -> Settings:
    return Settings(
        database_url="postgresql+psycopg://user@postgres:5432/db",
        redis_url="redis://redis:6379/0",
        dependency_check_timeout_seconds=0.5,
    )


@pytest.fixture
def release() -> Iterator[threading.Event]:
    """An event a blocked probe waits on; always released at the end of the test."""
    event = threading.Event()
    yield event
    event.set()

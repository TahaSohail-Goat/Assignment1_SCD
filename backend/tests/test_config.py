"""Settings come from the environment and have no default connection string."""

import pytest
from pydantic import ValidationError

from app.config import Settings


def test_the_connection_strings_are_required(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("DATABASE_URL", raising=False)
    monkeypatch.delenv("REDIS_URL", raising=False)

    with pytest.raises(ValidationError) as error:
        Settings()  # type: ignore[call-arg]

    missing = {issue["loc"][0] for issue in error.value.errors()}
    assert missing == {"database_url", "redis_url"}


def test_settings_are_read_from_the_environment(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("DATABASE_URL", "postgresql+psycopg://u@postgres:5432/d")
    monkeypatch.setenv("REDIS_URL", "redis://redis:6379/0")
    monkeypatch.setenv("LOG_LEVEL", "DEBUG")

    settings = Settings()  # type: ignore[call-arg]

    assert settings.database_url.endswith("/d")
    assert settings.redis_url == "redis://redis:6379/0"
    assert settings.log_level == "DEBUG"

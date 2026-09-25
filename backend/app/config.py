"""Settings, read from the environment.

The two connection strings have no default on purpose: a default would be a
credential or a ``localhost`` address in the source, and a missing value must
stop the process at start instead of failing later (ASG-DED-001, ASG-NFR-016).
"""

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(extra="ignore")

    database_url: str
    redis_url: str
    log_level: str = "INFO"
    dependency_check_timeout_seconds: float = 1.0


@lru_cache
def get_settings() -> Settings:
    return Settings()

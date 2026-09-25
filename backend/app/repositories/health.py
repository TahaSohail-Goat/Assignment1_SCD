"""Database reachability probe. All SQL lives in repositories (ASG-NFR-005)."""

from sqlalchemy import Engine, text


class DatabaseHealthRepository:
    name = "postgres"

    def __init__(self, engine: Engine) -> None:
        self._engine = engine

    def check(self) -> None:
        """Raise if PostgreSQL cannot answer a trivial query."""
        with self._engine.connect() as connection:
            connection.execute(text("SELECT 1"))

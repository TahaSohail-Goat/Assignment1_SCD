"""ASG-DATA-002…004, 016, 017: the schema comes from reversible Alembic migrations."""

import pytest
from alembic import command
from alembic.autogenerate import compare_metadata
from alembic.migration import MigrationContext
from sqlalchemy import Engine, inspect, text
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.repositories.models import Base
from tests.db import alembic_config, reset_schema

pytestmark = pytest.mark.integration

EXPECTED_COLUMNS = {
    "id",
    "text",
    "location",
    "reporter_contact",
    "category",
    "priority",
    "status",
    "ai_summary",
    "triaged_by",
    "triage_latency_ms",
    "created_at",
    "updated_at",
}


def _tables(engine: Engine) -> set[str]:
    return set(inspect(engine).get_table_names())


def _enum_types(engine: Engine) -> set[str]:
    with engine.connect() as connection:
        rows = connection.execute(text("SELECT typname FROM pg_type WHERE typtype = 'e'")).all()
    return {row[0] for row in rows}


def test_upgrade_and_downgrade_both_work_on_an_empty_database(engine: Engine, db_url: str) -> None:
    config = alembic_config(db_url)
    reset_schema(engine)

    command.upgrade(config, "head")
    assert "complaints" in _tables(engine)
    assert _enum_types(engine) == {"complaint_category", "complaint_priority", "complaint_status"}

    command.downgrade(config, "base")
    assert "complaints" not in _tables(engine)
    assert _enum_types(engine) == set()

    command.upgrade(config, "head")  # and up again: the migration is repeatable
    assert "complaints" in _tables(engine)


def test_the_schema_has_exactly_the_columns_of_the_assignment(migrated: Engine) -> None:
    columns = {c["name"]: c for c in inspect(migrated).get_columns("complaints")}

    assert set(columns) == EXPECTED_COLUMNS
    assert columns["reporter_contact"]["nullable"] is True
    assert columns["ai_summary"]["nullable"] is True
    assert columns["status"]["default"] is not None and "open" in columns["status"]["default"]
    with migrated.connect() as connection:
        types = dict(
            connection.execute(
                text(
                    "SELECT column_name, data_type FROM information_schema.columns "
                    "WHERE table_name = 'complaints'"
                )
            ).all()
        )
    assert types["id"] == "uuid"
    assert types["created_at"] == "timestamp with time zone"
    assert types["updated_at"] == "timestamp with time zone"
    assert types["triage_latency_ms"] == "integer"


def test_the_two_required_indexes_exist(migrated: Engine) -> None:
    indexes = {i["name"]: i["column_names"] for i in inspect(migrated).get_indexes("complaints")}

    assert indexes["ix_complaints_status_priority"] == ["status", "priority"]
    assert indexes["ix_complaints_created_at"] == ["created_at"]


def test_the_orm_models_match_the_migrated_database(migrated: Engine) -> None:
    with migrated.connect() as connection:
        differences = compare_metadata(MigrationContext.configure(connection), Base.metadata)

    assert differences == []


@pytest.mark.parametrize(
    ("column", "value"),
    [
        ("text", "x" * 9),  # the assignment's example: a 9-character text is rejected
        ("text", "x" * 2001),
        ("location", "ab"),
        ("location", "y" * 201),
        ("ai_summary", "s" * 141),
        ("ai_summary", "two\nlines"),
        ("triaged_by", "bogus"),
        ("triaged_by", "llm:"),
        ("triage_latency_ms", -1),
    ],
)
def test_the_database_itself_rejects_values_the_assignment_forbids(
    session: Session, column: str, value: object
) -> None:
    row = {
        "text": "x" * 20,
        "location": "Sector 4",
        "category": "water",
        "priority": "high",
        "ai_summary": "one line",
        "triaged_by": "rules",
        "triage_latency_ms": 5,
    }
    row[column] = value  # type: ignore[assignment]
    names = ", ".join(row)
    binds = ", ".join(f":{name}" for name in row)

    with pytest.raises(IntegrityError), session.begin_nested():
        session.execute(text(f"INSERT INTO complaints ({names}) VALUES ({binds})"), row)  # noqa: S608  (names come from this test)


@pytest.mark.parametrize(
    "value", ["rules", "rules:fallback", "simulated", "llm:groq", "llm:ollama", "llm:gemini"]
)
def test_the_database_accepts_every_triaged_by_value_of_the_design(
    session: Session, value: str
) -> None:
    session.execute(
        text(
            "INSERT INTO complaints (text, location, category, priority, triaged_by, triage_latency_ms) "
            "VALUES (:t, :l, 'roads', 'low', :v, 1)"
        ),
        {"t": "x" * 12, "l": "Main road", "v": value},
    )

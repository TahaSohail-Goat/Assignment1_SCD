"""The complaint repository against a real PostgreSQL (ASG-DATA-005…015, ASG-FR-024…026)."""

import uuid
from datetime import UTC, datetime, timedelta

import pytest
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.domain import Category, Priority, Status
from app.repositories.complaints import ComplaintFilters, SqlComplaintRepository
from tests.db import new_complaint

pytestmark = pytest.mark.integration


def _spread_creation_times(session: Session) -> None:
    """Rows of one transaction share now(); give them distinct times, oldest first by text."""
    session.execute(
        text(
            "UPDATE complaints c SET created_at = TIMESTAMPTZ '2026-01-01 00:00:00+00' "
            "+ (n.rn * INTERVAL '1 minute') "
            "FROM (SELECT id, row_number() OVER (ORDER BY text) AS rn FROM complaints) n "
            "WHERE c.id = n.id"
        )
    )


def test_add_returns_the_stored_complaint_with_server_generated_values(session: Session) -> None:
    repository = SqlComplaintRepository(session)

    record = repository.add(new_complaint(reporter_contact="0300-1234567"))

    assert isinstance(record.id, uuid.UUID)
    assert record.status is Status.OPEN
    assert record.category is Category.WATER
    assert record.priority is Priority.HIGH
    assert record.reporter_contact == "0300-1234567"
    assert record.created_at.tzinfo is not None
    assert record.created_at.utcoffset() == timedelta(0)
    assert abs(record.created_at - datetime.now(UTC)) < timedelta(minutes=1)
    assert record.updated_at == record.created_at


def test_get_returns_the_complaint_or_none(session: Session) -> None:
    repository = SqlComplaintRepository(session)
    added = repository.add(new_complaint())

    assert repository.get(added.id) == added
    assert repository.get(uuid.uuid4()) is None


def test_list_page_filters_combine_with_and_and_total_counts_the_matches(session: Session) -> None:
    repository = SqlComplaintRepository(session)
    repository.add(
        new_complaint(text="water high a" * 2, category=Category.WATER, priority=Priority.HIGH)
    )
    repository.add(
        new_complaint(text="water low b" * 2, category=Category.WATER, priority=Priority.LOW)
    )
    repository.add(
        new_complaint(text="roads high c" * 2, category=Category.ROADS, priority=Priority.HIGH)
    )

    only_water, total_water = repository.list_page(ComplaintFilters(category=Category.WATER), 1, 20)
    water_high, total_water_high = repository.list_page(
        ComplaintFilters(category=Category.WATER, priority=Priority.HIGH), 1, 20
    )
    none, total_none = repository.list_page(ComplaintFilters(status=Status.RESOLVED), 1, 20)

    assert (len(only_water), total_water) == (2, 2)
    assert (len(water_high), total_water_high) == (1, 1)
    assert water_high[0].category is Category.WATER and water_high[0].priority is Priority.HIGH
    assert (none, total_none) == ([], 0)


def test_list_page_is_newest_first_paged_without_overlap_and_total_is_the_full_count(
    session: Session,
) -> None:
    repository = SqlComplaintRepository(session)
    for number in range(25):
        repository.add(new_complaint(text=f"complaint number {number:02d} of the batch"))
    _spread_creation_times(session)

    first, total = repository.list_page(ComplaintFilters(), 1, 10)
    second, _ = repository.list_page(ComplaintFilters(), 2, 10)
    third, _ = repository.list_page(ComplaintFilters(), 3, 10)
    beyond, total_beyond = repository.list_page(ComplaintFilters(), 4, 10)

    assert total == 25 and total_beyond == 25
    assert [len(first), len(second), len(third), len(beyond)] == [10, 10, 5, 0]
    everyone = first + second + third
    assert len({r.id for r in everyone}) == 25
    assert [r.created_at for r in everyone] == sorted(
        (r.created_at for r in everyone), reverse=True
    )
    assert everyone[0].text.endswith("24 of the batch")  # the newest is the last one created


def test_update_status_changes_it_only_when_the_expected_status_still_holds(
    session: Session,
) -> None:
    repository = SqlComplaintRepository(session)
    added = repository.add(new_complaint())

    moved = repository.update_status(added.id, Status.OPEN, Status.IN_PROGRESS)
    stale = repository.update_status(added.id, Status.OPEN, Status.REJECTED)
    unknown = repository.update_status(uuid.uuid4(), Status.OPEN, Status.IN_PROGRESS)

    assert moved is not None and moved.status is Status.IN_PROGRESS
    assert moved.updated_at >= added.updated_at
    assert stale is None
    assert unknown is None
    stored = repository.get(added.id)
    assert stored is not None and stored.status is Status.IN_PROGRESS


def test_counts_group_by_category_and_priority(session: Session) -> None:
    repository = SqlComplaintRepository(session)
    repository.add(new_complaint(text="a" * 12, category=Category.WATER, priority=Priority.HIGH))
    repository.add(new_complaint(text="b" * 12, category=Category.WATER, priority=Priority.LOW))
    repository.add(new_complaint(text="c" * 12, category=Category.ROADS, priority=Priority.LOW))

    counts = repository.counts()

    assert counts.total == 3
    assert counts.by_category == {Category.WATER: 2, Category.ROADS: 1}
    assert counts.by_priority == {Priority.HIGH: 1, Priority.LOW: 2}


def test_recent_outcomes_are_the_newest_twenty_with_provider_and_latency(session: Session) -> None:
    repository = SqlComplaintRepository(session)
    for number in range(23):
        repository.add(
            new_complaint(
                text=f"outcome number {number:02d} of the batch",
                triaged_by="rules:fallback" if number % 2 else "llm:groq",
                triage_latency_ms=number,
            )
        )
    _spread_creation_times(session)

    outcomes = repository.recent_outcomes()

    assert len(outcomes) == 20
    assert outcomes[0].latency_ms == 22  # newest first
    assert outcomes[0].provider == "llm:groq"
    assert outcomes[1].provider == "rules:fallback"


def test_add_many_if_absent_is_idempotent(session: Session) -> None:
    repository = SqlComplaintRepository(session)
    fixed = [uuid.UUID(int=n + 1) for n in range(3)]
    batch = [new_complaint(id=i, text=f"seed complaint number {n}") for n, i in enumerate(fixed)]

    first = repository.add_many_if_absent(batch)
    second = repository.add_many_if_absent(batch)
    total = repository.counts().total

    assert (first, second, total) == (3, 0, 3)


def test_add_many_if_absent_needs_a_fixed_id_for_every_complaint(session: Session) -> None:
    repository = SqlComplaintRepository(session)

    with pytest.raises(ValueError, match="fixed id"):
        repository.add_many_if_absent([new_complaint()])

    assert repository.add_many_if_absent([]) == 0

"""Seed content and repeatability (ASG-DATA-019…021)."""

import uuid

import pytest
from sqlalchemy.orm import Session

from app.domain import Category, Priority
from app.repositories.complaints import SqlComplaintRepository
from app.seed import SEED_ROWS, seed_items


def test_seed_has_thirty_distinct_synthetic_complaints_across_all_values() -> None:
    items = seed_items()

    assert len(items) >= 30
    assert len({item.id for item in items}) == len(items)
    assert len({item.text for item in items}) == len(items)
    assert {item.category for item in items} == set(Category)
    assert {item.priority for item in items} == set(Priority)
    assert all(item.reporter_contact is None for item in items)
    assert all(10 <= len(item.text) <= 2000 and 3 <= len(item.location) <= 200 for item in items)
    assert all(isinstance(item.id, uuid.UUID) for item in items)
    assert len(SEED_ROWS) == 30


def test_seed_ids_are_stable_between_runs() -> None:
    assert [item.id for item in seed_items()] == [item.id for item in seed_items()]


@pytest.mark.integration
def test_seed_twice_inserts_only_thirty_rows(session: Session) -> None:
    repository = SqlComplaintRepository(session)

    first = repository.add_many_if_absent(seed_items())
    second = repository.add_many_if_absent(seed_items())

    assert first == 30
    assert second == 0
    assert repository.counts().total == 30

"""The complaint service against in-memory fakes: rules without a database or a network."""

import uuid

import pytest

from app.domain import Category, Priority, Status
from app.errors import InvalidTransitionError, NotFoundError
from app.repositories.complaints import ComplaintFilters
from app.services.complaints import ComplaintService, NewComplaintInput, parse_complaint_id
from tests.fakes import FakeUnitOfWork, InMemoryComplaints, RacingComplaints, StubTriager

DATA = NewComplaintInput(
    text="The street light on our lane has been out for a week.",
    location="Lane 3, Gulberg",
    reporter_contact=None,
)


def _service(
    repository: InMemoryComplaints | None = None,
) -> tuple[ComplaintService, FakeUnitOfWork, StubTriager]:
    unit_of_work = FakeUnitOfWork(repository)
    triager = StubTriager()
    return ComplaintService(unit_of_work, triager), unit_of_work, triager


def test_create_triages_then_persists_in_one_committed_transaction() -> None:
    service, unit_of_work, triager = _service()

    record = service.create(DATA)

    assert triager.calls == [(DATA.text, DATA.location)]
    assert record.category is Category.WATER and record.priority is Priority.HIGH
    assert record.triaged_by == "simulated" and record.triage_latency_ms == 7
    assert record.status is Status.OPEN
    assert unit_of_work.repository.rows == {record.id: record}
    assert (unit_of_work.commits, unit_of_work.rollbacks) == (1, 0)


def test_a_triage_failure_persists_nothing() -> None:
    class Failing:
        def triage(self, text: str, location: str) -> object:
            raise RuntimeError("provider down")

    unit_of_work = FakeUnitOfWork()
    service = ComplaintService(unit_of_work, Failing())  # type: ignore[arg-type]

    with pytest.raises(RuntimeError):
        service.create(DATA)

    assert unit_of_work.repository.rows == {}


def test_get_returns_the_complaint_and_raises_not_found_for_unknown_or_malformed_ids() -> None:
    service, _, _ = _service()
    created = service.create(DATA)

    assert service.get(str(created.id)) == created
    with pytest.raises(NotFoundError):
        service.get(str(uuid.uuid4()))
    with pytest.raises(NotFoundError):
        service.get("not-a-uuid")


def test_parse_complaint_id_treats_a_malformed_id_as_not_found() -> None:
    known = uuid.uuid4()

    assert parse_complaint_id(str(known)) == known
    with pytest.raises(NotFoundError):
        parse_complaint_id("12345")


def test_list_passes_filters_and_paging_to_the_repository() -> None:
    service, _, _ = _service()
    for _ in range(3):
        service.create(DATA)

    records, total = service.list(ComplaintFilters(status=Status.OPEN), 2, 2)

    assert (len(records), total) == (1, 3)


def test_change_status_applies_an_allowed_transition() -> None:
    service, unit_of_work, _ = _service()
    created = service.create(DATA)

    moved = service.change_status(str(created.id), Status.IN_PROGRESS)
    resolved = service.change_status(str(created.id), Status.RESOLVED)

    assert moved.status is Status.IN_PROGRESS
    assert resolved.status is Status.RESOLVED
    assert unit_of_work.repository.rows[created.id].status is Status.RESOLVED


def test_change_status_refuses_a_forbidden_transition_and_leaves_the_complaint_alone() -> None:
    service, unit_of_work, _ = _service()
    created = service.create(DATA)

    with pytest.raises(InvalidTransitionError):
        service.change_status(str(created.id), Status.RESOLVED)  # open -> resolved is not allowed

    assert unit_of_work.repository.rows[created.id].status is Status.OPEN
    assert unit_of_work.rollbacks == 1


def test_change_status_on_an_unknown_id_is_not_found() -> None:
    service, _, _ = _service()

    with pytest.raises(NotFoundError):
        service.change_status(str(uuid.uuid4()), Status.IN_PROGRESS)


def test_a_concurrent_change_is_noticed_and_the_rule_is_checked_again() -> None:
    repository = RacingComplaints(changed_to=Status.REJECTED)
    service, _, _ = _service(repository)
    created = service.create(DATA)

    # Between the read and the update another request rejected the complaint; a terminal
    # status cannot move to in_progress, so the second check refuses instead of overwriting.
    with pytest.raises(InvalidTransitionError):
        service.change_status(str(created.id), Status.IN_PROGRESS)

    assert repository.rows[created.id].status is Status.REJECTED


def test_a_concurrent_change_that_still_allows_the_move_is_applied_on_the_retry() -> None:
    repository = RacingComplaints(changed_to=Status.IN_PROGRESS)
    service, _, _ = _service(repository)
    created = service.create(DATA)

    # open -> rejected is allowed, and so is in_progress -> rejected, so the retry succeeds.
    rejected = service.change_status(str(created.id), Status.REJECTED)

    assert rejected.status is Status.REJECTED

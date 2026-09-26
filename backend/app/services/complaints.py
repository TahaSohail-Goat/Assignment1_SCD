"""Business rules for complaints: create, read, list and change status.

The services know nothing about HTTP or SQL. They talk to a ``Triager`` (implemented by the
triage packages) and, through a unit of work, to the repository protocol.
"""

import uuid
from collections.abc import Callable
from dataclasses import dataclass
from typing import Protocol

from app.domain import Category, Priority, Status
from app.errors import NotFoundError
from app.repositories.complaints import (
    ComplaintFilters,
    ComplaintRecord,
    NewComplaint,
)
from app.repositories.uow import UnitOfWork
from app.services.state_machine import check_transition

MAX_STATUS_ATTEMPTS = 3


@dataclass(frozen=True)
class TriageDecision:
    """What triage returns to the complaint service (the model of assignment section 2.5,
    plus the provider name and the measured latency that the database stores)."""

    category: Category
    priority: Priority
    ai_summary: str | None
    triaged_by: str
    latency_ms: int


class Triager(Protocol):
    def triage(self, text: str, location: str, complaint_id: uuid.UUID) -> TriageDecision: ...


@dataclass(frozen=True)
class NewComplaintInput:
    text: str
    location: str
    reporter_contact: str | None


def parse_complaint_id(raw: str) -> uuid.UUID:
    """A malformed id is treated as an id that does not exist (docs/API_DESIGN.md, DQ-API-06)."""
    try:
        return uuid.UUID(raw)
    except ValueError:
        raise NotFoundError() from None


class ComplaintService:
    def __init__(
        self,
        unit_of_work: Callable[[], UnitOfWork],
        triager: Triager,
        after_create: Callable[[], None] | None = None,
    ) -> None:
        self._unit_of_work = unit_of_work
        self._triager = triager
        self._after_create = after_create  # runs once the new complaint is committed

    def create(self, data: NewComplaintInput) -> ComplaintRecord:
        """Triage the complaint, then persist it (validate -> triage -> persist, section 2.2)."""
        complaint_id = uuid.uuid4()  # known before triage, so a fallback warning can name it
        decision = self._triager.triage(data.text, data.location, complaint_id)
        new = NewComplaint(
            id=complaint_id,
            text=data.text,
            location=data.location,
            reporter_contact=data.reporter_contact,
            category=decision.category,
            priority=decision.priority,
            ai_summary=decision.ai_summary,
            triaged_by=decision.triaged_by,
            triage_latency_ms=decision.latency_ms,
        )
        with self._unit_of_work() as repository:
            record = repository.add(new)
        if self._after_create is not None:
            self._after_create()  # for example: drop the cached statistics
        return record

    def get(self, raw_id: str) -> ComplaintRecord:
        complaint_id = parse_complaint_id(raw_id)
        with self._unit_of_work() as repository:
            record = repository.get(complaint_id)
        if record is None:
            raise NotFoundError()
        return record

    def list(
        self, filters: ComplaintFilters, page: int, page_size: int
    ) -> tuple[list[ComplaintRecord], int]:
        with self._unit_of_work() as repository:
            return repository.list_page(filters, page, page_size)

    def change_status(self, raw_id: str, target: Status) -> ComplaintRecord:
        """Apply the state machine. The update names the status it expects, so a concurrent
        change is noticed: the complaint is read again and the rule is checked again."""
        complaint_id = parse_complaint_id(raw_id)
        with self._unit_of_work() as repository:
            for _attempt in range(MAX_STATUS_ATTEMPTS):
                current = repository.get(complaint_id)
                if current is None:
                    raise NotFoundError()
                check_transition(current.status, target)
                updated = repository.update_status(complaint_id, current.status, target)
                if updated is not None:
                    return updated
            latest = repository.get(complaint_id)
            if latest is None:
                raise NotFoundError()
            check_transition(latest.status, target)
            raise RuntimeError("the status kept changing under concurrent updates")

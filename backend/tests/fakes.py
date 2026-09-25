"""In-memory stand-ins for the repository, the unit of work and the triage provider.

They let the services and the HTTP layer be tested without a database or a network.
"""

import uuid
from collections.abc import Sequence
from dataclasses import replace
from datetime import UTC, datetime, timedelta
from types import TracebackType

from app.domain import Category, Priority, Status
from app.repositories.complaints import (
    ComplaintFilters,
    ComplaintRecord,
    NewComplaint,
    StatsCounts,
    TriageOutcome,
)
from app.services.complaints import TriageDecision

EPOCH = datetime(2026, 1, 1, tzinfo=UTC)


class InMemoryComplaints:
    def __init__(self) -> None:
        self.rows: dict[uuid.UUID, ComplaintRecord] = {}
        self._tick = 0

    def add(self, new: NewComplaint) -> ComplaintRecord:
        self._tick += 1
        moment = EPOCH + timedelta(minutes=self._tick)
        record = ComplaintRecord(
            id=new.id or uuid.uuid4(),
            text=new.text,
            location=new.location,
            reporter_contact=new.reporter_contact,
            category=new.category,
            priority=new.priority,
            status=Status.OPEN,
            ai_summary=new.ai_summary,
            triaged_by=new.triaged_by,
            triage_latency_ms=new.triage_latency_ms,
            created_at=moment,
            updated_at=moment,
        )
        self.rows[record.id] = record
        return record

    def add_many_if_absent(self, items: Sequence[NewComplaint]) -> int:
        added = 0
        for item in items:
            if item.id not in self.rows:
                self.add(item)
                added += 1
        return added

    def get(self, complaint_id: uuid.UUID) -> ComplaintRecord | None:
        return self.rows.get(complaint_id)

    def list_page(
        self, filters: ComplaintFilters, page: int, page_size: int
    ) -> tuple[list[ComplaintRecord], int]:
        matching = [
            record
            for record in self.rows.values()
            if (filters.category is None or record.category == filters.category)
            and (filters.priority is None or record.priority == filters.priority)
            and (filters.status is None or record.status == filters.status)
        ]
        matching.sort(key=lambda record: (record.created_at, str(record.id)), reverse=True)
        start = (page - 1) * page_size
        return matching[start : start + page_size], len(matching)

    def update_status(
        self, complaint_id: uuid.UUID, expected: Status, new: Status
    ) -> ComplaintRecord | None:
        current = self.rows.get(complaint_id)
        if current is None or current.status != expected:
            return None
        updated = replace(current, status=new, updated_at=current.updated_at + timedelta(seconds=1))
        self.rows[complaint_id] = updated
        return updated

    def counts(self) -> StatsCounts:
        raise NotImplementedError

    def recent_outcomes(self, limit: int = 20) -> list[TriageOutcome]:
        raise NotImplementedError


class RacingComplaints(InMemoryComplaints):
    """Another request changes the status between the read and the guarded update."""

    def __init__(self, changed_to: Status) -> None:
        super().__init__()
        self._changed_to = changed_to
        self._raced = False

    def update_status(
        self, complaint_id: uuid.UUID, expected: Status, new: Status
    ) -> ComplaintRecord | None:
        if not self._raced:
            self._raced = True
            self.rows[complaint_id] = replace(self.rows[complaint_id], status=self._changed_to)
        return super().update_status(complaint_id, expected, new)


class FakeUnitOfWork:
    """Callable like the unit-of-work factory; counts commits and rollbacks."""

    def __init__(self, repository: InMemoryComplaints | None = None) -> None:
        self.repository = repository or InMemoryComplaints()
        self.commits = 0
        self.rollbacks = 0

    def __call__(self) -> "FakeUnitOfWork":
        return self

    def __enter__(self) -> InMemoryComplaints:
        return self.repository

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        if exc_type is None:
            self.commits += 1
        else:
            self.rollbacks += 1


class StubTriager:
    def __init__(self, decision: TriageDecision | None = None) -> None:
        self.decision = decision or TriageDecision(
            category=Category.WATER,
            priority=Priority.HIGH,
            ai_summary="No water for three days",
            triaged_by="simulated",
            latency_ms=7,
        )
        self.calls: list[tuple[str, str]] = []
        self.ids: list[uuid.UUID] = []

    def triage(self, text: str, location: str, complaint_id: uuid.UUID) -> TriageDecision:
        self.calls.append((text, location))
        self.ids.append(complaint_id)
        return self.decision

"""In-memory stand-ins for the repository, the unit of work and the triage provider.

They let the services and the HTTP layer be tested without a database or a network.
"""

import uuid
from collections.abc import Sequence
from dataclasses import replace
from datetime import UTC, datetime, timedelta
from types import TracebackType

from app.domain import Category, Priority, Status
from app.providers.cache import CacheUnavailableError
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
        by_category: dict[Category, int] = {}
        by_priority: dict[Priority, int] = {}
        for record in self.rows.values():
            by_category[record.category] = by_category.get(record.category, 0) + 1
            by_priority[record.priority] = by_priority.get(record.priority, 0) + 1
        return StatsCounts(len(self.rows), by_category, by_priority)

    def recent_outcomes(self, limit: int = 20) -> list[TriageOutcome]:
        newest = sorted(self.rows.values(), key=lambda r: (r.created_at, str(r.id)), reverse=True)
        return [
            TriageOutcome(r.id, r.triaged_by, r.triage_latency_ms, r.created_at)
            for r in newest[:limit]
        ]


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


class FakeCache:
    """A key-value cache with a TTL measured on a clock the test moves by hand (no sleeping)."""

    def __init__(self) -> None:
        self.now = 0.0
        self.down = False
        self.sets: list[tuple[str, int]] = []
        self.deletes = 0
        self._data: dict[str, tuple[str, float]] = {}

    def _check(self) -> None:
        if self.down:
            raise CacheUnavailableError("ConnectionError")

    def advance(self, seconds: float) -> None:
        self.now += seconds

    def get(self, key: str) -> str | None:
        self._check()
        item = self._data.get(key)
        if item is None:
            return None
        value, expires_at = item
        if self.now >= expires_at:
            del self._data[key]
            return None
        return value

    def set(self, key: str, value: str, ttl_seconds: int) -> None:
        self._check()
        self._data[key] = (value, self.now + ttl_seconds)
        self.sets.append((key, ttl_seconds))

    def delete(self, key: str) -> None:
        self._check()
        self.deletes += 1
        self._data.pop(key, None)

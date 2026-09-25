"""Complaint persistence. All SQL of the application lives in this package (ASG-NFR-005).

The services depend on the ``ComplaintRepository`` protocol and on plain records, never on
ORM objects or sessions, so the rules of the state machine and of triage stay testable
without a database. The repository never commits: the caller owns the transaction.
"""

import uuid
from collections.abc import Sequence
from dataclasses import dataclass
from datetime import UTC, datetime
from typing import Protocol

from sqlalchemy import func, select, update
from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlalchemy.orm import Session

from app.domain import Category, Priority, Status
from app.repositories.models import ComplaintRow


@dataclass(frozen=True)
class NewComplaint:
    text: str
    location: str
    reporter_contact: str | None
    category: Category
    priority: Priority
    ai_summary: str | None
    triaged_by: str
    triage_latency_ms: int
    id: uuid.UUID | None = None  # None: the database generates it; the seed sets a fixed one


@dataclass(frozen=True)
class ComplaintRecord:
    id: uuid.UUID
    text: str
    location: str
    reporter_contact: str | None
    category: Category
    priority: Priority
    status: Status
    ai_summary: str | None
    triaged_by: str
    triage_latency_ms: int
    created_at: datetime
    updated_at: datetime


@dataclass(frozen=True)
class ComplaintFilters:
    category: Category | None = None
    priority: Priority | None = None
    status: Status | None = None


@dataclass(frozen=True)
class StatsCounts:
    total: int
    by_category: dict[Category, int]
    by_priority: dict[Priority, int]


@dataclass(frozen=True)
class TriageOutcome:
    complaint_id: uuid.UUID
    provider: str
    latency_ms: int
    at: datetime


class ComplaintRepository(Protocol):
    def add(self, new: NewComplaint) -> ComplaintRecord: ...

    def add_many_if_absent(self, items: Sequence[NewComplaint]) -> int: ...

    def get(self, complaint_id: uuid.UUID) -> ComplaintRecord | None: ...

    def list_page(
        self, filters: ComplaintFilters, page: int, page_size: int
    ) -> tuple[list[ComplaintRecord], int]: ...

    def update_status(
        self, complaint_id: uuid.UUID, expected: Status, new: Status
    ) -> ComplaintRecord | None: ...

    def counts(self) -> StatsCounts: ...

    def recent_outcomes(self, limit: int = 20) -> list[TriageOutcome]: ...


def _utc(value: datetime) -> datetime:
    return value.astimezone(UTC)


def _record(row: ComplaintRow) -> ComplaintRecord:
    return ComplaintRecord(
        id=row.id,
        text=row.text,
        location=row.location,
        reporter_contact=row.reporter_contact,
        category=Category(row.category),
        priority=Priority(row.priority),
        status=Status(row.status),
        ai_summary=row.ai_summary,
        triaged_by=row.triaged_by,
        triage_latency_ms=row.triage_latency_ms,
        created_at=_utc(row.created_at),
        updated_at=_utc(row.updated_at),
    )


def _values(new: NewComplaint) -> dict[str, object]:
    values: dict[str, object] = {
        "text": new.text,
        "location": new.location,
        "reporter_contact": new.reporter_contact,
        "category": new.category.value,
        "priority": new.priority.value,
        "ai_summary": new.ai_summary,
        "triaged_by": new.triaged_by,
        "triage_latency_ms": new.triage_latency_ms,
    }
    if new.id is not None:
        values["id"] = new.id
    return values


class SqlComplaintRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def add(self, new: NewComplaint) -> ComplaintRecord:
        row = ComplaintRow(**_values(new))
        self._session.add(row)
        self._session.flush()
        self._session.refresh(row)  # picks up the server-generated id and timestamps
        return _record(row)

    def add_many_if_absent(self, items: Sequence[NewComplaint]) -> int:
        """Insert complaints that have a fixed id, skipping the ones already present.

        Used by the seed command: running it twice adds nothing (ASG-DATA-021).
        """
        if any(item.id is None for item in items):
            raise ValueError("every complaint to seed needs a fixed id")
        if not items:
            return 0
        statement = (
            pg_insert(ComplaintRow)
            .values([_values(item) for item in items])
            .on_conflict_do_nothing(index_elements=["id"])
            .returning(ComplaintRow.id)
        )
        return len(self._session.execute(statement).all())

    def get(self, complaint_id: uuid.UUID) -> ComplaintRecord | None:
        row = self._session.get(ComplaintRow, complaint_id)
        return _record(row) if row is not None else None

    def list_page(
        self, filters: ComplaintFilters, page: int, page_size: int
    ) -> tuple[list[ComplaintRecord], int]:
        conditions = []
        if filters.category is not None:
            conditions.append(ComplaintRow.category == filters.category.value)
        if filters.priority is not None:
            conditions.append(ComplaintRow.priority == filters.priority.value)
        if filters.status is not None:
            conditions.append(ComplaintRow.status == filters.status.value)
        total = self._session.execute(
            select(func.count()).select_from(ComplaintRow).where(*conditions)
        ).scalar_one()
        rows = self._session.scalars(
            select(ComplaintRow)
            .where(*conditions)
            .order_by(ComplaintRow.created_at.desc(), ComplaintRow.id)
            .limit(page_size)
            .offset((page - 1) * page_size)
        ).all()
        return [_record(row) for row in rows], total

    def update_status(
        self, complaint_id: uuid.UUID, expected: Status, new: Status
    ) -> ComplaintRecord | None:
        """Change the status only if it is still ``expected``; None when nothing matched."""
        row = self._session.execute(
            update(ComplaintRow)
            .where(ComplaintRow.id == complaint_id, ComplaintRow.status == expected.value)
            .values(status=new.value, updated_at=func.now())
            .returning(ComplaintRow)
            .execution_options(populate_existing=True)
        ).scalar_one_or_none()
        return _record(row) if row is not None else None

    def counts(self) -> StatsCounts:
        by_category = {
            Category(name): count
            for name, count in self._session.execute(
                select(ComplaintRow.category, func.count()).group_by(ComplaintRow.category)
            ).all()
        }
        by_priority = {
            Priority(name): count
            for name, count in self._session.execute(
                select(ComplaintRow.priority, func.count()).group_by(ComplaintRow.priority)
            ).all()
        }
        return StatsCounts(
            total=sum(by_category.values()), by_category=by_category, by_priority=by_priority
        )

    def recent_outcomes(self, limit: int = 20) -> list[TriageOutcome]:
        rows = self._session.execute(
            select(
                ComplaintRow.id,
                ComplaintRow.triaged_by,
                ComplaintRow.triage_latency_ms,
                ComplaintRow.created_at,
            )
            .order_by(ComplaintRow.created_at.desc(), ComplaintRow.id)
            .limit(limit)
        ).all()
        return [
            TriageOutcome(complaint_id=r[0], provider=r[1], latency_ms=r[2], at=_utc(r[3]))
            for r in rows
        ]

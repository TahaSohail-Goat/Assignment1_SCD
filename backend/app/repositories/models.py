"""ORM description of the schema. The migrations are the source of the DDL, never this file.

A test compares these models with the migrated database, so the two cannot drift apart.
"""

import uuid
from datetime import datetime

from sqlalchemy import CheckConstraint, DateTime, Index, Integer, Text
from sqlalchemy import text as sql_text
from sqlalchemy.dialects import postgresql
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from app.domain import (
    AI_SUMMARY_MAX,
    LOCATION_MAX,
    LOCATION_MIN,
    TEXT_MAX,
    TEXT_MIN,
    Category,
    Priority,
    Status,
)

CATEGORY_TYPE = postgresql.ENUM(
    *[c.value for c in Category], name="complaint_category", create_type=False
)
PRIORITY_TYPE = postgresql.ENUM(
    *[p.value for p in Priority], name="complaint_priority", create_type=False
)
STATUS_TYPE = postgresql.ENUM(
    *[s.value for s in Status], name="complaint_status", create_type=False
)

TRIAGED_BY_CHECK = (
    "triaged_by IN ('rules', 'rules:fallback', 'simulated') "
    "OR triaged_by ~ '^llm:[a-z0-9][a-z0-9_.-]*$'"
)


class Base(DeclarativeBase):
    pass


class ComplaintRow(Base):
    __tablename__ = "complaints"

    id: Mapped[uuid.UUID] = mapped_column(
        postgresql.UUID(as_uuid=True),
        primary_key=True,
        server_default=sql_text("gen_random_uuid()"),
    )
    text: Mapped[str] = mapped_column(Text, nullable=False)
    location: Mapped[str] = mapped_column(Text, nullable=False)
    reporter_contact: Mapped[str | None] = mapped_column(Text, nullable=True)
    category: Mapped[str] = mapped_column(CATEGORY_TYPE, nullable=False)
    priority: Mapped[str] = mapped_column(PRIORITY_TYPE, nullable=False)
    status: Mapped[str] = mapped_column(
        STATUS_TYPE, nullable=False, server_default=sql_text("'open'")
    )
    ai_summary: Mapped[str | None] = mapped_column(Text, nullable=True)
    triaged_by: Mapped[str] = mapped_column(Text, nullable=False)
    triage_latency_ms: Mapped[int] = mapped_column(Integer, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=sql_text("now()")
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=sql_text("now()")
    )

    __table_args__ = (
        CheckConstraint(
            f"char_length(text) BETWEEN {TEXT_MIN} AND {TEXT_MAX}", name="ck_complaints_text_length"
        ),
        CheckConstraint(
            f"char_length(location) BETWEEN {LOCATION_MIN} AND {LOCATION_MAX}",
            name="ck_complaints_location_length",
        ),
        CheckConstraint(
            f"ai_summary IS NULL OR (char_length(ai_summary) <= {AI_SUMMARY_MAX} "
            "AND ai_summary !~ '[\\r\\n]')",
            name="ck_complaints_ai_summary_one_line",
        ),
        CheckConstraint(TRIAGED_BY_CHECK, name="ck_complaints_triaged_by"),
        CheckConstraint("triage_latency_ms >= 0", name="ck_complaints_triage_latency_ms"),
        Index("ix_complaints_status_priority", "status", "priority"),
        Index("ix_complaints_created_at", "created_at"),
    )

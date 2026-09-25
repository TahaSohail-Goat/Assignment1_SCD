"""create the complaints table

The minimum schema of assignment section 2.3 (ASG-DATA-005 to ASG-DATA-017): a
server-generated UUID, the length limits enforced in the database as well as in the
application, the three enums, timestamptz columns, and the two required indexes.

Revision ID: 0001
Revises:
Create Date: 2026-09-25
"""

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision = "0001"
down_revision = None
branch_labels = None
depends_on = None

CATEGORIES = ("water", "electricity", "sanitation", "roads", "streetlights", "other")
PRIORITIES = ("high", "normal", "low")
STATUSES = ("open", "in_progress", "resolved", "rejected")


def _enum(name: str, values: tuple[str, ...]) -> postgresql.ENUM:
    return postgresql.ENUM(*values, name=name, create_type=False)


def upgrade() -> None:
    bind = op.get_bind()
    for name, values in (
        ("complaint_category", CATEGORIES),
        ("complaint_priority", PRIORITIES),
        ("complaint_status", STATUSES),
    ):
        postgresql.ENUM(*values, name=name).create(bind, checkfirst=True)

    op.create_table(
        "complaints",
        sa.Column(
            "id",
            postgresql.UUID(as_uuid=True),
            primary_key=True,
            server_default=sa.text("gen_random_uuid()"),
        ),
        sa.Column("text", sa.Text(), nullable=False),
        sa.Column("location", sa.Text(), nullable=False),
        sa.Column("reporter_contact", sa.Text(), nullable=True),
        sa.Column("category", _enum("complaint_category", CATEGORIES), nullable=False),
        sa.Column("priority", _enum("complaint_priority", PRIORITIES), nullable=False),
        sa.Column(
            "status",
            _enum("complaint_status", STATUSES),
            nullable=False,
            server_default=sa.text("'open'"),
        ),
        sa.Column("ai_summary", sa.Text(), nullable=True),
        sa.Column("triaged_by", sa.Text(), nullable=False),
        sa.Column("triage_latency_ms", sa.Integer(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.text("now()"),
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.text("now()"),
        ),
        sa.CheckConstraint(
            "char_length(text) BETWEEN 10 AND 2000", name="ck_complaints_text_length"
        ),
        sa.CheckConstraint(
            "char_length(location) BETWEEN 3 AND 200", name="ck_complaints_location_length"
        ),
        sa.CheckConstraint(
            "ai_summary IS NULL OR (char_length(ai_summary) <= 140 AND ai_summary !~ '[\\r\\n]')",
            name="ck_complaints_ai_summary_one_line",
        ),
        sa.CheckConstraint(
            "triaged_by IN ('rules', 'rules:fallback', 'simulated') "
            "OR triaged_by ~ '^llm:[a-z0-9][a-z0-9_.-]*$'",
            name="ck_complaints_triaged_by",
        ),
        sa.CheckConstraint("triage_latency_ms >= 0", name="ck_complaints_triage_latency_ms"),
    )
    op.create_index("ix_complaints_status_priority", "complaints", ["status", "priority"])
    op.create_index("ix_complaints_created_at", "complaints", ["created_at"])


def downgrade() -> None:
    op.drop_index("ix_complaints_created_at", table_name="complaints")
    op.drop_index("ix_complaints_status_priority", table_name="complaints")
    op.drop_table("complaints")
    bind = op.get_bind()
    for name in ("complaint_status", "complaint_priority", "complaint_category"):
        postgresql.ENUM(name=name).drop(bind, checkfirst=True)

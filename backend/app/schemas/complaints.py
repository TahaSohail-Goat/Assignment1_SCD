"""Pydantic models for the complaint endpoints. Field names equal the column names (DQ-API-05)."""

import uuid
from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

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
from app.repositories.complaints import ComplaintRecord

CONTACT_MAX = 200  # not fixed by the assignment: a design decision (docs/API_DESIGN.md, section 3)


class ComplaintCreate(BaseModel):
    model_config = ConfigDict(extra="ignore", str_strip_whitespace=True)

    text: str = Field(min_length=TEXT_MIN, max_length=TEXT_MAX)
    location: str = Field(min_length=LOCATION_MIN, max_length=LOCATION_MAX)
    reporter_contact: str | None = Field(default=None, max_length=CONTACT_MAX)


class StatusUpdate(BaseModel):
    model_config = ConfigDict(extra="ignore")

    status: Status


class Complaint(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    text: str
    location: str
    reporter_contact: str | None
    category: Category
    priority: Priority
    status: Status
    ai_summary: str | None = Field(max_length=AI_SUMMARY_MAX)
    triaged_by: str
    triage_latency_ms: int
    created_at: datetime
    updated_at: datetime

    @classmethod
    def from_record(cls, record: ComplaintRecord) -> "Complaint":
        return cls.model_validate(record)


class ComplaintPage(BaseModel):
    items: list[Complaint]
    total: int
    page: int
    page_size: int


class ErrorDetail(BaseModel):
    code: str
    message: str
    details: list[dict[str, Any]] | None = None


class ErrorResponse(BaseModel):
    error: ErrorDetail

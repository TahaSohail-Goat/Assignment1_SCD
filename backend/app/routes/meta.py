"""Recent provider outcomes from persisted complaints (ASG-FR-030)."""

from datetime import datetime
from collections.abc import Callable
from uuid import UUID

from fastapi import APIRouter, Request
from pydantic import BaseModel, Field

from app.repositories.uow import UnitOfWork

router = APIRouter(prefix="/api/meta", tags=["meta"])


class TriageOutcome(BaseModel):
    complaint_id: UUID
    provider: str
    latency_ms: int
    fallback: bool
    at: datetime


class ProvidersMeta(BaseModel):
    active_provider: str
    recent: list[TriageOutcome] = Field(max_length=20)


@router.get("/providers", response_model=ProvidersMeta)
def get_providers(request: Request) -> ProvidersMeta:
    open_unit_of_work: Callable[[], UnitOfWork] = request.app.state.unit_of_work
    with open_unit_of_work() as repository:
        outcomes = repository.recent_outcomes(20)
    return ProvidersMeta(
        active_provider=request.app.state.active_provider,
        recent=[
            TriageOutcome(
                complaint_id=item.complaint_id,
                provider=item.provider,
                latency_ms=item.latency_ms,
                fallback=item.provider == "rules:fallback",
                at=item.at,
            )
            for item in outcomes
        ],
    )

"""The complaint endpoints (ASG-FR-020, 021, 023, 024, 025, 026, 027, 028).

HTTP only: parse, validate, serialise, status codes. No business rule and no database session.
"""

from typing import Annotated

from fastapi import APIRouter, Depends, Query, Request, Response

from app.domain import Category, Priority, Status
from app.repositories.complaints import ComplaintFilters
from app.schemas.complaints import (
    Complaint,
    ComplaintCreate,
    ComplaintPage,
    ErrorResponse,
    StatusUpdate,
)
from app.services.complaints import ComplaintService, NewComplaintInput

router = APIRouter(prefix="/api/complaints", tags=["complaints"])

MAX_PAGE_SIZE = 100  # assignment section 2.2 p6
DEFAULT_PAGE_SIZE = 20  # a design decision (docs/API_DESIGN.md, DQ-API-03)

_ERRORS: dict[int | str, dict[str, object]] = {
    400: {"model": ErrorResponse, "description": "Validation error"},
    404: {"model": ErrorResponse, "description": "Complaint not found"},
    409: {"model": ErrorResponse, "description": "Invalid status transition"},
    429: {"model": ErrorResponse, "description": "Rate limit exceeded"},
}


def get_service(request: Request) -> ComplaintService:
    service: ComplaintService = request.app.state.complaints
    return service


ServiceDep = Annotated[ComplaintService, Depends(get_service)]


@router.post(
    "",
    status_code=201,
    response_model=Complaint,
    responses={code: _ERRORS[code] for code in (400, 429)},
)
def create_complaint(body: ComplaintCreate, service: ServiceDep, response: Response) -> Complaint:
    record = service.create(
        NewComplaintInput(
            text=body.text, location=body.location, reporter_contact=body.reporter_contact
        )
    )
    response.headers["Location"] = f"/api/complaints/{record.id}"
    return Complaint.from_record(record)


@router.get("", response_model=ComplaintPage, responses={400: _ERRORS[400]})
def list_complaints(
    service: ServiceDep,
    category: Category | None = None,
    priority: Priority | None = None,
    status: Status | None = None,
    page: Annotated[int, Query(ge=1)] = 1,
    page_size: Annotated[int, Query(ge=1, le=MAX_PAGE_SIZE)] = DEFAULT_PAGE_SIZE,
) -> ComplaintPage:
    records, total = service.list(
        ComplaintFilters(category=category, priority=priority, status=status), page, page_size
    )
    return ComplaintPage(
        items=[Complaint.from_record(record) for record in records],
        total=total,
        page=page,
        page_size=page_size,
    )


@router.get("/{complaint_id}", response_model=Complaint, responses={404: _ERRORS[404]})
def get_complaint(complaint_id: str, service: ServiceDep) -> Complaint:
    return Complaint.from_record(service.get(complaint_id))


@router.patch(
    "/{complaint_id}/status",
    response_model=Complaint,
    responses={code: _ERRORS[code] for code in (400, 404, 409)},
)
def change_status(complaint_id: str, body: StatusUpdate, service: ServiceDep) -> Complaint:
    return Complaint.from_record(service.change_status(complaint_id, body.status))

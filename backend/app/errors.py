"""Domain errors and the shape of the error body (docs/API_DESIGN.md, section 1).

This module has no HTTP framework in it: the services raise these errors, and
``app/http_errors.py`` turns them into responses.
"""

from typing import Any

from app.domain import Status


def error_body(
    code: str, message: str, details: list[dict[str, Any]] | None = None
) -> dict[str, Any]:
    error: dict[str, Any] = {"code": code, "message": message}
    if details is not None:
        error["details"] = details
    return {"error": error}


class DomainError(Exception):
    """Base of the errors the services raise on purpose."""


class NotFoundError(DomainError):
    """The complaint does not exist (a malformed id counts as one that does not exist)."""

    def __init__(self, what: str = "Complaint") -> None:
        super().__init__(f"{what} not found")
        self.what = what


class InvalidTransitionError(DomainError):
    """The requested status change is not in the transition table (ASG-FR-028)."""

    def __init__(self, current: Status, target: Status) -> None:
        super().__init__(f"Cannot change status from {current.value} to {target.value}")
        self.current = current
        self.target = target

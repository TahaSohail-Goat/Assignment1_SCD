"""The complaint status machine, as explicit data (ASG-FR-034, ASG-FR-035).

open -> in_progress -> resolved; open -> rejected; in_progress -> rejected.
``resolved`` and ``rejected`` are terminal. Everything else, including a change to the
status a complaint already has, is refused (assignment section 2.2 p6: "Everything else is 409").
"""

from app.domain import Status
from app.errors import InvalidTransitionError

TRANSITIONS: dict[Status, frozenset[Status]] = {
    Status.OPEN: frozenset({Status.IN_PROGRESS, Status.REJECTED}),
    Status.IN_PROGRESS: frozenset({Status.RESOLVED, Status.REJECTED}),
    Status.RESOLVED: frozenset(),
    Status.REJECTED: frozenset(),
}


def is_allowed(current: Status, target: Status) -> bool:
    return target in TRANSITIONS[current]


def check_transition(current: Status, target: Status) -> None:
    """Raise ``InvalidTransitionError`` naming the attempted transition when it is not allowed."""
    if not is_allowed(current, target):
        raise InvalidTransitionError(current, target)

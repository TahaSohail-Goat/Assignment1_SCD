"""ASG-FR-034 and ASG-FR-035: the status machine, as explicit data, over all 16 pairs."""

import itertools

import pytest

from app.domain import Status
from app.errors import InvalidTransitionError
from app.services.state_machine import TRANSITIONS, check_transition, is_allowed

ALLOWED = {
    (Status.OPEN, Status.IN_PROGRESS),
    (Status.OPEN, Status.REJECTED),
    (Status.IN_PROGRESS, Status.RESOLVED),
    (Status.IN_PROGRESS, Status.REJECTED),
}
ALL_PAIRS = list(itertools.product(Status, Status))


def test_the_transition_table_is_data_covering_every_status() -> None:
    assert set(TRANSITIONS) == set(Status)
    assert all(isinstance(targets, frozenset) for targets in TRANSITIONS.values())


def test_there_are_sixteen_pairs_four_allowed_and_twelve_forbidden() -> None:
    assert len(ALL_PAIRS) == 16
    assert sum(is_allowed(a, b) for a, b in ALL_PAIRS) == 4


@pytest.mark.parametrize(("current", "target"), ALL_PAIRS)
def test_each_pair_behaves_as_the_assignment_says(current: Status, target: Status) -> None:
    if (current, target) in ALLOWED:
        check_transition(current, target)  # no error
        assert is_allowed(current, target)
    else:
        with pytest.raises(InvalidTransitionError) as error:
            check_transition(current, target)
        assert str(error.value) == f"Cannot change status from {current.value} to {target.value}"
        assert (error.value.current, error.value.target) == (current, target)


@pytest.mark.parametrize("terminal", [Status.RESOLVED, Status.REJECTED])
def test_resolved_and_rejected_are_terminal(terminal: Status) -> None:
    assert not any(is_allowed(terminal, other) for other in Status)

"""Read provider outcomes through the repository boundary."""

from collections.abc import Callable

from app.repositories.complaints import TriageOutcome
from app.repositories.uow import UnitOfWork


class MetaService:
    def __init__(self, unit_of_work: Callable[[], UnitOfWork]) -> None:
        self._unit_of_work = unit_of_work

    def recent_outcomes(self) -> list[TriageOutcome]:
        with self._unit_of_work() as repository:
            return repository.recent_outcomes(20)

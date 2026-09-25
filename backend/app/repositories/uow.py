"""Unit of work: one transaction per service operation, opened and closed outside the routes.

The services ask for a repository inside a ``with`` block; the transaction commits when the
block ends normally and rolls back when it raises. Services see only the repository protocol.
"""

from types import TracebackType
from typing import Protocol

from sqlalchemy.orm import Session, sessionmaker

from app.repositories.complaints import ComplaintRepository, SqlComplaintRepository


class UnitOfWork(Protocol):
    def __enter__(self) -> ComplaintRepository: ...

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        traceback: TracebackType | None,
    ) -> None: ...


class SqlUnitOfWork:
    def __init__(self, session_factory: sessionmaker[Session]) -> None:
        self._session_factory = session_factory
        self._session: Session | None = None

    def __enter__(self) -> ComplaintRepository:
        self._session = self._session_factory()
        return SqlComplaintRepository(self._session)

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        if self._session is None:
            raise RuntimeError("the unit of work was never entered")
        try:
            if exc_type is None:
                self._session.commit()
            else:
                self._session.rollback()
        finally:
            self._session.close()
            self._session = None

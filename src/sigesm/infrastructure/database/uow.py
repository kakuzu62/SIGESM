from __future__ import annotations

from contextlib import AbstractContextManager
from types import TracebackType

from sqlalchemy.orm import Session

from sigesm.application.ports import UnitOfWork
from sigesm.infrastructure.database.session import DatabaseSessionFactory


class SqlAlchemyUnitOfWork(UnitOfWork):
    def __init__(self, session: Session) -> None:
        self.session = session

    def __enter__(self) -> SqlAlchemyUnitOfWork:
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        if exc_type is not None:
            self.rollback()
        self.session.close()

    def commit(self) -> None:
        self.session.commit()

    def rollback(self) -> None:
        self.session.rollback()


class SqlAlchemyUnitOfWorkFactory:
    def __init__(self, session_factory: DatabaseSessionFactory) -> None:
        self._session_factory = session_factory

    def create(self) -> SqlAlchemyUnitOfWork:
        session_context = self._session_factory.create()
        session = session_context.__enter__()
        return _ContextManagedSqlAlchemyUnitOfWork(session=session, session_context=session_context)


class _ContextManagedSqlAlchemyUnitOfWork(SqlAlchemyUnitOfWork):
    def __init__(self, session: Session, session_context: AbstractContextManager[Session]) -> None:
        super().__init__(session=session)
        self._session_context = session_context

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        if exc_type is not None:
            self.rollback()
        self._session_context.__exit__(exc_type, exc, traceback)

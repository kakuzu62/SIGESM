from __future__ import annotations

from types import TracebackType

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from core.database.session import DatabaseSessionFactory
from domain.identity.repositories import IUserRepository
from infrastructure.persistence.sqlalchemy.identity.repositories import SqlAlchemyUserRepository
from infrastructure.persistence.sqlalchemy.session_context import SessionContext
from presentation.modules.user_management.application.commands.change_user_status.unit_of_work import (
    UserStatusConflictError,
    UserStatusUnitOfWork,
    UserStatusUnitOfWorkFactory,
)


class SqlAlchemyUserStatusUnitOfWork(UserStatusUnitOfWork):
    """SQLAlchemy Unit of Work for user active status changes."""

    def __init__(self, session_context: SessionContext) -> None:
        self._session_context = session_context
        self._session: Session | None = None
        self._users: SqlAlchemyUserRepository | None = None

    @property
    def users(self) -> IUserRepository:
        """Return the SQLAlchemy user repository bound to the active session."""
        if self._users is None:
            raise RuntimeError("User status Unit of Work is not open.")
        return self._users

    def __enter__(self) -> SqlAlchemyUserStatusUnitOfWork:
        self._session = self._session_context.__enter__()
        self._users = SqlAlchemyUserRepository(self._session)
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        self._session_context.__exit__(exc_type, exc, traceback)
        self._session = None
        self._users = None

    def commit(self) -> None:
        """Commit the status change."""
        if self._session is None:
            raise RuntimeError("User status Unit of Work is not open.")
        try:
            self._session.commit()
        except SQLAlchemyError as exc:
            raise UserStatusConflictError("User status persistence failed.") from exc

    def rollback(self) -> None:
        """Rollback the status change."""
        if self._session is not None:
            self._session.rollback()


class SqlAlchemyUserStatusUnitOfWorkFactory(UserStatusUnitOfWorkFactory):
    """Factory for SQLAlchemy user status Unit of Work instances."""

    def __init__(self, session_factory: DatabaseSessionFactory) -> None:
        self._session_factory = session_factory

    def create(self) -> SqlAlchemyUserStatusUnitOfWork:
        """Create a SQLAlchemy Unit of Work."""
        return SqlAlchemyUserStatusUnitOfWork(SessionContext(self._session_factory))

from __future__ import annotations

from contextlib import AbstractContextManager
from types import TracebackType

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from core.database.session import DatabaseSessionFactory
from domain.identity.repositories import IUserRepository
from infrastructure.persistence.sqlalchemy.identity.repositories import SqlAlchemyUserRepository
from infrastructure.persistence.sqlalchemy.session_context import SessionContext
from presentation.modules.user_management.application.commands.update_user.unit_of_work import (
    UserUpdateConflictError,
    UserUpdateUnitOfWork,
    UserUpdateUnitOfWorkFactory,
)


class SqlAlchemyUserUpdateUnitOfWork(UserUpdateUnitOfWork):
    """SQLAlchemy Unit of Work for user profile editing."""

    def __init__(self, session_context: AbstractContextManager[Session]) -> None:
        self._session_context = session_context
        self._session: Session | None = None
        self._users: SqlAlchemyUserRepository | None = None

    @property
    def users(self) -> IUserRepository:
        """Return the SQLAlchemy user repository bound to the active session."""
        if self._session is None:
            raise RuntimeError("Unit of Work must be entered before accessing repositories.")
        if self._users is None:
            self._users = SqlAlchemyUserRepository(self._session)
        return self._users

    def __enter__(self) -> SqlAlchemyUserUpdateUnitOfWork:
        self._session = self._session_context.__enter__()
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        if exc_type is not None:
            self.rollback()
        self._session_context.__exit__(exc_type, exc, traceback)

    def commit(self) -> None:
        """Commit the SQLAlchemy transaction."""
        if self._session is None:
            raise RuntimeError("Unit of Work must be entered before commit.")
        try:
            self._session.commit()
        except IntegrityError as exc:
            self._session.rollback()
            raise UserUpdateConflictError("Unique user constraint violated.") from exc

    def rollback(self) -> None:
        """Rollback the SQLAlchemy transaction."""
        if self._session is not None:
            self._session.rollback()


class SqlAlchemyUserUpdateUnitOfWorkFactory(UserUpdateUnitOfWorkFactory):
    """Factory for SQLAlchemy user update Unit of Work instances."""

    def __init__(self, session_factory: DatabaseSessionFactory) -> None:
        self._session_factory = session_factory

    def create(self) -> SqlAlchemyUserUpdateUnitOfWork:
        """Create a Unit of Work using a fresh session context."""
        return SqlAlchemyUserUpdateUnitOfWork(SessionContext(self._session_factory))

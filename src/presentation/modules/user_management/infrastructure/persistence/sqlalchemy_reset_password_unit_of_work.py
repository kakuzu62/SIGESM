from __future__ import annotations

from types import TracebackType

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from core.database.session import DatabaseSessionFactory
from domain.identity.repositories import IUserRepository
from infrastructure.persistence.sqlalchemy.identity.repositories import SqlAlchemyUserRepository
from infrastructure.persistence.sqlalchemy.session_context import SessionContext
from presentation.modules.user_management.application.commands.reset_password.unit_of_work import (
    PasswordResetPersistenceError,
    ResetPasswordUnitOfWork,
    ResetPasswordUnitOfWorkFactory,
)


class SqlAlchemyResetPasswordUnitOfWork(ResetPasswordUnitOfWork):
    """SQLAlchemy Unit of Work for administrator password reset."""

    def __init__(self, session_context: SessionContext) -> None:
        self._session_context = session_context
        self._session: Session | None = None
        self._users: SqlAlchemyUserRepository | None = None

    @property
    def users(self) -> IUserRepository:
        """Return the SQLAlchemy user repository bound to the active session."""
        if self._users is None:
            raise RuntimeError("Reset password Unit of Work is not open.")
        return self._users

    def __enter__(self) -> SqlAlchemyResetPasswordUnitOfWork:
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
        """Commit the password reset."""
        if self._session is None:
            raise RuntimeError("Reset password Unit of Work is not open.")
        try:
            self._session.commit()
        except SQLAlchemyError as exc:
            raise PasswordResetPersistenceError("Password reset persistence failed.") from exc

    def rollback(self) -> None:
        """Rollback the password reset."""
        if self._session is not None:
            self._session.rollback()


class SqlAlchemyResetPasswordUnitOfWorkFactory(ResetPasswordUnitOfWorkFactory):
    """Factory for SQLAlchemy password reset Unit of Work instances."""

    def __init__(self, session_factory: DatabaseSessionFactory) -> None:
        self._session_factory = session_factory

    def create(self) -> SqlAlchemyResetPasswordUnitOfWork:
        """Create a SQLAlchemy Unit of Work."""
        return SqlAlchemyResetPasswordUnitOfWork(SessionContext(self._session_factory))

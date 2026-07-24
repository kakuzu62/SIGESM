from __future__ import annotations

from types import TracebackType

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from core.database.session import DatabaseSessionFactory
from domain.identity.repositories import IRoleRepository, IUserRepository
from infrastructure.persistence.sqlalchemy.identity.repositories import (
    SqlAlchemyRoleRepository,
    SqlAlchemyUserRepository,
)
from infrastructure.persistence.sqlalchemy.session_context import SessionContext
from presentation.modules.user_management.application.commands.assign_user_roles.unit_of_work import (
    UserRolesPersistenceError,
    UserRolesUnitOfWork,
    UserRolesUnitOfWorkFactory,
)


class SqlAlchemyUserRolesUnitOfWork(UserRolesUnitOfWork):
    """SQLAlchemy Unit of Work for user role assignments."""

    def __init__(self, session_context: SessionContext) -> None:
        self._session_context = session_context
        self._session: Session | None = None
        self._users: SqlAlchemyUserRepository | None = None
        self._roles: SqlAlchemyRoleRepository | None = None

    @property
    def users(self) -> IUserRepository:
        """Return user repository bound to the active session."""
        if self._users is None:
            raise RuntimeError("User roles Unit of Work is not open.")
        return self._users

    @property
    def roles(self) -> IRoleRepository:
        """Return role repository bound to the active session."""
        if self._roles is None:
            raise RuntimeError("User roles Unit of Work is not open.")
        return self._roles

    def __enter__(self) -> SqlAlchemyUserRolesUnitOfWork:
        self._session = self._session_context.__enter__()
        self._users = SqlAlchemyUserRepository(self._session)
        self._roles = SqlAlchemyRoleRepository(self._session)
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
        self._roles = None

    def commit(self) -> None:
        """Commit the assignment."""
        if self._session is None:
            raise RuntimeError("User roles Unit of Work is not open.")
        try:
            self._session.commit()
        except SQLAlchemyError as exc:
            raise UserRolesPersistenceError("User roles persistence failed.") from exc

    def rollback(self) -> None:
        """Rollback the assignment."""
        if self._session is not None:
            self._session.rollback()


class SqlAlchemyUserRolesUnitOfWorkFactory(UserRolesUnitOfWorkFactory):
    """Factory for SQLAlchemy user roles Unit of Work instances."""

    def __init__(self, session_factory: DatabaseSessionFactory) -> None:
        self._session_factory = session_factory

    def create(self) -> SqlAlchemyUserRolesUnitOfWork:
        """Create a SQLAlchemy Unit of Work."""
        return SqlAlchemyUserRolesUnitOfWork(SessionContext(self._session_factory))

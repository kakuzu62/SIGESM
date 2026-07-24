from __future__ import annotations

from types import TracebackType
from typing import Protocol

from domain.identity.repositories import IRoleRepository, IUserRepository


class UserRolesPersistenceError(Exception):
    """Raised when role assignment persistence fails."""


class UserRolesUnitOfWork(Protocol):
    """Unit of Work contract for assigning user roles."""

    @property
    def users(self) -> IUserRepository:
        """Return user repository bound to the active transaction."""
        raise NotImplementedError

    @property
    def roles(self) -> IRoleRepository:
        """Return role repository bound to the active transaction."""
        raise NotImplementedError

    def __enter__(self) -> UserRolesUnitOfWork:
        """Open the Unit of Work."""
        raise NotImplementedError

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        """Close the Unit of Work."""
        raise NotImplementedError

    def commit(self) -> None:
        """Commit the role assignment."""
        raise NotImplementedError

    def rollback(self) -> None:
        """Rollback the role assignment."""
        raise NotImplementedError


class UserRolesUnitOfWorkFactory(Protocol):
    """Factory for user roles Unit of Work instances."""

    def create(self) -> UserRolesUnitOfWork:
        """Create a Unit of Work."""
        raise NotImplementedError

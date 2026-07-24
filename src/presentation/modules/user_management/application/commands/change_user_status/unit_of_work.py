from __future__ import annotations

from types import TracebackType
from typing import Protocol

from domain.identity.repositories import IUserRepository


class UserStatusConflictError(Exception):
    """Raised when status persistence conflicts with current database state."""


class UserStatusUnitOfWork(Protocol):
    """Unit of Work contract for user active status changes."""

    @property
    def users(self) -> IUserRepository:
        """Return user repository bound to the active transaction."""
        raise NotImplementedError

    def __enter__(self) -> UserStatusUnitOfWork:
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
        """Commit the status change."""
        raise NotImplementedError

    def rollback(self) -> None:
        """Rollback the status change."""
        raise NotImplementedError


class UserStatusUnitOfWorkFactory(Protocol):
    """Factory for user status Unit of Work instances."""

    def create(self) -> UserStatusUnitOfWork:
        """Create a Unit of Work."""
        raise NotImplementedError

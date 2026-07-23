from __future__ import annotations

from types import TracebackType
from typing import Protocol

from domain.identity.repositories import IUserRepository


class UserUpdateConflictError(Exception):
    """Raised when persistence detects a unique user constraint conflict."""


class UserUpdateUnitOfWork(Protocol):
    """Unit of Work contract required by the update user use case."""

    @property
    def users(self) -> IUserRepository:
        """Return the user repository bound to this transaction."""
        raise NotImplementedError

    def __enter__(self) -> UserUpdateUnitOfWork:
        raise NotImplementedError

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        raise NotImplementedError

    def commit(self) -> None:
        """Commit the transaction."""
        raise NotImplementedError

    def rollback(self) -> None:
        """Rollback the transaction."""
        raise NotImplementedError


class UserUpdateUnitOfWorkFactory(Protocol):
    """Factory for user update Unit of Work instances."""

    def create(self) -> UserUpdateUnitOfWork:
        """Create a new Unit of Work."""
        raise NotImplementedError

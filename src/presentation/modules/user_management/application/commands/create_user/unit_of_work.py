from __future__ import annotations

from types import TracebackType
from typing import Protocol

from domain.identity.repositories import IUserRepository


class UserCreationConflictError(Exception):
    """Raised when persistence detects a unique user constraint conflict."""


class UserCreationUnitOfWork(Protocol):
    """Unit of Work contract required by the create user use case."""

    @property
    def users(self) -> IUserRepository:
        """Return the user repository bound to this transaction."""
        raise NotImplementedError

    def __enter__(self) -> UserCreationUnitOfWork:
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


class UserCreationUnitOfWorkFactory(Protocol):
    """Factory for user creation Unit of Work instances."""

    def create(self) -> UserCreationUnitOfWork:
        """Create a new Unit of Work."""
        raise NotImplementedError

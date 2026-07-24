from __future__ import annotations

from types import TracebackType
from typing import Protocol

from domain.identity.repositories import IUserRepository


class PasswordResetPersistenceError(Exception):
    """Raised when password reset persistence fails."""


class ResetPasswordUnitOfWork(Protocol):
    """Unit of Work contract for administrator password reset."""

    @property
    def users(self) -> IUserRepository:
        """Return user repository bound to the active transaction."""
        raise NotImplementedError

    def __enter__(self) -> ResetPasswordUnitOfWork:
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
        """Commit the password reset."""
        raise NotImplementedError

    def rollback(self) -> None:
        """Rollback the password reset."""
        raise NotImplementedError


class ResetPasswordUnitOfWorkFactory(Protocol):
    """Factory for password reset Unit of Work instances."""

    def create(self) -> ResetPasswordUnitOfWork:
        """Create a Unit of Work."""
        raise NotImplementedError

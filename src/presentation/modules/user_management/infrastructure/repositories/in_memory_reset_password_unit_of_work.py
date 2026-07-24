from __future__ import annotations

from types import TracebackType

from domain.identity.repositories import IUserRepository
from infrastructure.identity import InMemoryUserRepository
from presentation.modules.user_management.application.commands.reset_password.unit_of_work import (
    ResetPasswordUnitOfWork,
    ResetPasswordUnitOfWorkFactory,
)


class InMemoryResetPasswordUnitOfWork(ResetPasswordUnitOfWork):
    """In-memory Unit of Work used by password reset tests and bootstrap."""

    def __init__(self, users: InMemoryUserRepository) -> None:
        self._users = users
        self.commits = 0
        self.rollbacks = 0

    @property
    def users(self) -> IUserRepository:
        """Return the in-memory user repository."""
        return self._users

    def __enter__(self) -> InMemoryResetPasswordUnitOfWork:
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        if exc_type is not None:
            self.rollback()

    def commit(self) -> None:
        """Record a successful commit."""
        self.commits += 1

    def rollback(self) -> None:
        """Record a rollback."""
        self.rollbacks += 1


class InMemoryResetPasswordUnitOfWorkFactory(ResetPasswordUnitOfWorkFactory):
    """Factory that reuses the desktop in-memory identity repository."""

    def __init__(self, users: InMemoryUserRepository) -> None:
        self._users = users
        self.created: list[InMemoryResetPasswordUnitOfWork] = []

    def create(self) -> InMemoryResetPasswordUnitOfWork:
        """Create a new in-memory Unit of Work."""
        unit_of_work = InMemoryResetPasswordUnitOfWork(self._users)
        self.created.append(unit_of_work)
        return unit_of_work

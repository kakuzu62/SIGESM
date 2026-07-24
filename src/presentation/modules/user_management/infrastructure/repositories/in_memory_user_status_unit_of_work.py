from __future__ import annotations

from types import TracebackType

from domain.identity.repositories import IUserRepository
from infrastructure.identity import InMemoryUserRepository
from presentation.modules.user_management.application.commands.change_user_status.unit_of_work import (
    UserStatusUnitOfWork,
    UserStatusUnitOfWorkFactory,
)


class InMemoryUserStatusUnitOfWork(UserStatusUnitOfWork):
    """In-memory Unit of Work used by user status tests and bootstrap."""

    def __init__(self, users: InMemoryUserRepository) -> None:
        self._users = users
        self.commits = 0
        self.rollbacks = 0

    @property
    def users(self) -> IUserRepository:
        """Return the in-memory user repository."""
        return self._users

    def __enter__(self) -> InMemoryUserStatusUnitOfWork:
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


class InMemoryUserStatusUnitOfWorkFactory(UserStatusUnitOfWorkFactory):
    """Factory that reuses the desktop in-memory identity repository."""

    def __init__(self, users: InMemoryUserRepository) -> None:
        self._users = users
        self.created: list[InMemoryUserStatusUnitOfWork] = []

    def create(self) -> InMemoryUserStatusUnitOfWork:
        """Create a new in-memory Unit of Work."""
        unit_of_work = InMemoryUserStatusUnitOfWork(self._users)
        self.created.append(unit_of_work)
        return unit_of_work

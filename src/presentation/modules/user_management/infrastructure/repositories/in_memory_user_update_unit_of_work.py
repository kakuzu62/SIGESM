from __future__ import annotations

from types import TracebackType

from domain.identity.repositories import IUserRepository
from infrastructure.identity import InMemoryUserRepository
from presentation.modules.user_management.application.commands.update_user.unit_of_work import (
    UserUpdateUnitOfWork,
    UserUpdateUnitOfWorkFactory,
)


class InMemoryUserUpdateUnitOfWork(UserUpdateUnitOfWork):
    """In-memory Unit of Work used by user editing tests and bootstrap."""

    def __init__(self, users: InMemoryUserRepository) -> None:
        self._users = users
        self.commits = 0
        self.rollbacks = 0

    @property
    def users(self) -> IUserRepository:
        """Return the in-memory user repository."""
        return self._users

    def __enter__(self) -> InMemoryUserUpdateUnitOfWork:
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


class InMemoryUserUpdateUnitOfWorkFactory(UserUpdateUnitOfWorkFactory):
    """Factory that reuses the desktop in-memory identity repository."""

    def __init__(self, users: InMemoryUserRepository) -> None:
        self._users = users
        self.created: list[InMemoryUserUpdateUnitOfWork] = []

    def create(self) -> InMemoryUserUpdateUnitOfWork:
        """Create a new in-memory Unit of Work."""
        unit_of_work = InMemoryUserUpdateUnitOfWork(self._users)
        self.created.append(unit_of_work)
        return unit_of_work

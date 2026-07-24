from __future__ import annotations

from types import TracebackType

from domain.identity.repositories import IRoleRepository, IUserRepository
from infrastructure.identity import InMemoryRoleRepository, InMemoryUserRepository
from presentation.modules.user_management.application.commands.assign_user_roles.unit_of_work import (
    UserRolesUnitOfWork,
    UserRolesUnitOfWorkFactory,
)


class InMemoryUserRolesUnitOfWork(UserRolesUnitOfWork):
    """In-memory Unit of Work used by user role assignment tests and bootstrap."""

    def __init__(self, users: InMemoryUserRepository, roles: InMemoryRoleRepository) -> None:
        self._users = users
        self._roles = roles
        self.commits = 0
        self.rollbacks = 0

    @property
    def users(self) -> IUserRepository:
        """Return the in-memory user repository."""
        return self._users

    @property
    def roles(self) -> IRoleRepository:
        """Return the in-memory role repository."""
        return self._roles

    def __enter__(self) -> InMemoryUserRolesUnitOfWork:
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


class InMemoryUserRolesUnitOfWorkFactory(UserRolesUnitOfWorkFactory):
    """Factory that reuses desktop in-memory identity repositories."""

    def __init__(self, users: InMemoryUserRepository, roles: InMemoryRoleRepository) -> None:
        self._users = users
        self._roles = roles
        self.created: list[InMemoryUserRolesUnitOfWork] = []

    def create(self) -> InMemoryUserRolesUnitOfWork:
        """Create a new in-memory Unit of Work."""
        unit_of_work = InMemoryUserRolesUnitOfWork(self._users, self._roles)
        self.created.append(unit_of_work)
        return unit_of_work

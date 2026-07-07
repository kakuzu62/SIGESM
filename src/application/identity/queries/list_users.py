from __future__ import annotations

from dataclasses import dataclass

from application.identity.dto import UserDTO
from domain.identity.repositories import IUserRepository


@dataclass(frozen=True, slots=True)
class ListUsersQuery:
    """Query used to list users."""

    include_inactive: bool = True


class ListUsersHandler:
    """List users query handler."""

    def __init__(self, users: IUserRepository) -> None:
        self._users = users

    def handle(self, query: ListUsersQuery) -> tuple[UserDTO, ...]:
        """Return users according to the requested filter."""
        users = self._users.list()
        filtered = users if query.include_inactive else tuple(user for user in users if user.active)
        return tuple(UserDTO.from_domain(user) for user in filtered)

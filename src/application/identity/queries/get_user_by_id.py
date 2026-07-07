from __future__ import annotations

from dataclasses import dataclass

from application.identity.dto import UserDTO
from domain.identity.repositories import IUserRepository
from shared.kernel.identity import Identity


@dataclass(frozen=True, slots=True)
class GetUserByIdQuery:
    """Query used to load a user by identity."""

    user_id: str


class GetUserByIdHandler:
    """Load user by id query handler."""

    def __init__(self, users: IUserRepository) -> None:
        self._users = users

    def handle(self, query: GetUserByIdQuery) -> UserDTO | None:
        """Return a user DTO when the user exists."""
        user = self._users.get_by_id(Identity.from_string(query.user_id))
        if user is None:
            return None

        return UserDTO.from_domain(user)

from __future__ import annotations

from dataclasses import dataclass

from application.identity.dto import UserDTO
from core.exceptions.application import ApplicationException
from domain.identity.repositories import IUserRepository
from shared.kernel.identity import Identity


@dataclass(frozen=True, slots=True)
class ActivateUserCommand:
    """Command used to activate a user."""

    user_id: str


class ActivateUserHandler:
    """Activate user use case."""

    def __init__(self, users: IUserRepository) -> None:
        self._users = users

    def handle(self, command: ActivateUserCommand) -> UserDTO:
        """Activate a user."""
        user = self._users.get_by_id(Identity.from_string(command.user_id))
        if user is None:
            raise ApplicationException("User was not found.")

        user.activate()
        self._users.update(user)
        return UserDTO.from_domain(user)

from __future__ import annotations

from dataclasses import dataclass

from application.identity.dto import UserDTO
from core.exceptions.application import ApplicationException
from domain.identity.repositories import IUserRepository
from shared.kernel.identity import Identity


@dataclass(frozen=True, slots=True)
class DeactivateUserCommand:
    """Command used to deactivate a user."""

    user_id: str
    reason: str


class DeactivateUserHandler:
    """Deactivate user use case."""

    def __init__(self, users: IUserRepository) -> None:
        self._users = users

    def handle(self, command: DeactivateUserCommand) -> UserDTO:
        """Deactivate a user."""
        user = self._users.get_by_id(Identity.from_string(command.user_id))
        if user is None:
            raise ApplicationException("User was not found.")

        user.deactivate(command.reason)
        self._users.update(user)
        return UserDTO.from_domain(user)

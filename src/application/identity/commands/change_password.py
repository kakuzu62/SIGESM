from __future__ import annotations

from dataclasses import dataclass

from application.identity.dto import UserDTO
from core.exceptions.application import ApplicationException
from domain.identity.repositories import IUserRepository
from domain.identity.services import PasswordService
from shared.kernel.identity import Identity


@dataclass(frozen=True, slots=True)
class ChangePasswordCommand:
    """Command used to change a user password."""

    user_id: str
    new_password: str


class ChangePasswordHandler:
    """Change password use case."""

    def __init__(self, users: IUserRepository, password_service: PasswordService) -> None:
        self._users = users
        self._password_service = password_service

    def handle(self, command: ChangePasswordCommand) -> UserDTO:
        """Change a user password."""
        user = self._users.get_by_id(Identity.from_string(command.user_id))
        if user is None:
            raise ApplicationException("User was not found.")

        user.change_password(self._password_service.hash_password(command.new_password))
        self._users.update(user)
        return UserDTO.from_domain(user)

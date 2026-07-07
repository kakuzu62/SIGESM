from __future__ import annotations

from dataclasses import dataclass

from application.identity.dto import UserDTO
from domain.identity.entities import User
from domain.identity.repositories import IUserRepository
from domain.identity.services import PasswordService
from domain.identity.value_objects import Email, Username


@dataclass(frozen=True, slots=True)
class CreateUserCommand:
    """Command used to create a user."""

    username: str
    email: str
    password: str


class CreateUserHandler:
    """Create user use case."""

    def __init__(self, users: IUserRepository, password_service: PasswordService) -> None:
        self._users = users
        self._password_service = password_service

    def handle(self, command: CreateUserCommand) -> UserDTO:
        """Create a user and persist it through the repository contract."""
        username = Username(command.username)
        email = Email(command.email)
        password_hash = self._password_service.hash_password(command.password)
        user = User.create(username, email, password_hash)
        self._users.add(user)
        return UserDTO.from_domain(user)

from __future__ import annotations

from dataclasses import dataclass

from application.identity.dto import AuthenticationDTO
from domain.identity.services import AuthenticationService
from domain.identity.value_objects import Username


@dataclass(frozen=True, slots=True)
class AuthenticateUserCommand:
    """Command used to authenticate a user."""

    username: str
    password: str


class AuthenticateUserHandler:
    """Authenticate user use case."""

    def __init__(self, authentication: AuthenticationService) -> None:
        self._authentication = authentication

    def handle(self, command: AuthenticateUserCommand) -> AuthenticationDTO:
        """Authenticate a user and return access credentials."""
        return AuthenticationDTO.from_tokens(
            self._authentication.authenticate(Username(command.username), command.password)
        )

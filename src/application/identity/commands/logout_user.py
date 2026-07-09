from __future__ import annotations

from dataclasses import dataclass

from domain.identity.services import AuthenticationService


@dataclass(frozen=True, slots=True)
class LogoutUserCommand:
    """Command used to logout a user."""

    access_token: str


class LogoutUserHandler:
    """Logout user use case."""

    def __init__(self, authentication: AuthenticationService) -> None:
        self._authentication = authentication

    def handle(self, command: LogoutUserCommand) -> None:
        """Logout a user by revoking the active access session."""
        self._authentication.logout(command.access_token)

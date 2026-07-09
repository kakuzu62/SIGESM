from __future__ import annotations

from application.identity.commands import AuthenticateUserCommand, AuthenticateUserHandler
from application.identity.dto import AuthenticationDTO


class LoginController:
    """Controller that connects the login view to the authentication use case."""

    def __init__(self, handler: AuthenticateUserHandler) -> None:
        self._handler = handler

    def authenticate(self, username: str, password: str) -> AuthenticationDTO:
        """Authenticate a user through the application layer."""
        return self._handler.handle(AuthenticateUserCommand(username=username, password=password))

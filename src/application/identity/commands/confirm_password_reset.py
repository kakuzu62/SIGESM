from __future__ import annotations

from dataclasses import dataclass

from domain.identity.services import AuthenticationService


@dataclass(frozen=True, slots=True)
class ConfirmPasswordResetCommand:
    """Command used to confirm password recovery."""

    reset_token: str
    new_password: str


class ConfirmPasswordResetHandler:
    """Confirm password reset use case."""

    def __init__(self, authentication: AuthenticationService) -> None:
        self._authentication = authentication

    def handle(self, command: ConfirmPasswordResetCommand) -> None:
        """Change the password using a valid reset token."""
        self._authentication.confirm_password_reset(command.reset_token, command.new_password)

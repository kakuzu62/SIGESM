from __future__ import annotations

from dataclasses import dataclass

from application.identity.dto import PasswordResetDTO
from domain.identity.services import AuthenticationService
from domain.identity.value_objects import Email


@dataclass(frozen=True, slots=True)
class RequestPasswordResetCommand:
    """Command used to request password recovery."""

    email: str


class RequestPasswordResetHandler:
    """Request password reset use case."""

    def __init__(self, authentication: AuthenticationService) -> None:
        self._authentication = authentication

    def handle(self, command: RequestPasswordResetCommand) -> PasswordResetDTO:
        """Create a reset request and return the reset token once."""
        token, request = self._authentication.request_password_reset(Email(command.email))
        return PasswordResetDTO.from_domain(token, request)

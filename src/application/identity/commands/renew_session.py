from __future__ import annotations

from dataclasses import dataclass

from application.identity.dto import AuthenticationDTO
from domain.identity.services import AuthenticationService


@dataclass(frozen=True, slots=True)
class RenewSessionCommand:
    """Command used to renew an authentication session."""

    refresh_token: str


class RenewSessionHandler:
    """Renew session use case."""

    def __init__(self, authentication: AuthenticationService) -> None:
        self._authentication = authentication

    def handle(self, command: RenewSessionCommand) -> AuthenticationDTO:
        """Renew an authentication session using a refresh token."""
        return AuthenticationDTO.from_tokens(
            self._authentication.renew_session(command.refresh_token)
        )

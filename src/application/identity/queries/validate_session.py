from __future__ import annotations

from dataclasses import dataclass

from application.identity.dto import SessionDTO
from domain.identity.services import AuthenticationService


@dataclass(frozen=True, slots=True)
class ValidateSessionQuery:
    """Query used to validate an access session."""

    access_token: str


class ValidateSessionHandler:
    """Validate session query handler."""

    def __init__(self, authentication: AuthenticationService) -> None:
        self._authentication = authentication

    def handle(self, query: ValidateSessionQuery) -> SessionDTO | None:
        """Return a session DTO when the access token is valid."""
        session = self._authentication.validate_session(query.access_token)
        if session is None:
            return None
        return SessionDTO.from_domain(session)

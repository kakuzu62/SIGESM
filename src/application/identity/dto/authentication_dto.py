from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from domain.identity.entities import AuthenticationSession, PasswordResetRequest
from domain.identity.services import AuthenticationTokens


@dataclass(frozen=True, slots=True)
class AuthenticationDTO:
    """Application DTO returned after authentication."""

    access_token: str
    refresh_token: str
    session_id: str
    refresh_session_id: str
    user_id: str
    expires_at: datetime
    refresh_expires_at: datetime

    @classmethod
    def from_tokens(cls, tokens: AuthenticationTokens) -> AuthenticationDTO:
        """Create an authentication DTO from generated tokens."""
        return cls(
            access_token=tokens.access_token,
            refresh_token=tokens.refresh_token,
            session_id=str(tokens.session.id),
            refresh_session_id=str(tokens.refresh_session.id),
            user_id=str(tokens.session.user_id),
            expires_at=tokens.session.expires_at,
            refresh_expires_at=tokens.refresh_session.expires_at,
        )


@dataclass(frozen=True, slots=True)
class SessionDTO:
    """Application DTO representing a validated session."""

    session_id: str
    user_id: str
    status: str
    expires_at: datetime

    @classmethod
    def from_domain(cls, session: AuthenticationSession) -> SessionDTO:
        """Create a DTO from an authentication session."""
        return cls(
            session_id=str(session.id),
            user_id=str(session.user_id),
            status=session.status.value,
            expires_at=session.expires_at,
        )


@dataclass(frozen=True, slots=True)
class PasswordResetDTO:
    """Application DTO returned when a reset request is created."""

    reset_token: str
    request_id: str
    user_id: str
    expires_at: datetime

    @classmethod
    def from_domain(cls, reset_token: str, request: PasswordResetRequest) -> PasswordResetDTO:
        """Create a password reset DTO."""
        return cls(
            reset_token=reset_token,
            request_id=str(request.id),
            user_id=str(request.user_id),
            expires_at=request.expires_at,
        )

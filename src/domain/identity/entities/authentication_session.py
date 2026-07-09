from __future__ import annotations

from datetime import UTC, datetime

from domain.identity.value_objects import SessionStatus
from shared.kernel.entity import Entity
from shared.kernel.identity import Identity


class AuthenticationSession(Entity[Identity]):
    """Authentication session persisted with a hashed access token."""

    __slots__ = ("_user_id", "_token_hash", "_status", "_created_at", "_expires_at", "_revoked_at")

    def __init__(
        self,
        entity_id: Identity,
        user_id: Identity,
        token_hash: str,
        status: SessionStatus,
        created_at: datetime,
        expires_at: datetime,
        revoked_at: datetime | None = None,
    ) -> None:
        super().__init__(entity_id)
        self._user_id = user_id
        self._token_hash = token_hash
        self._status = status
        self._created_at = created_at
        self._expires_at = expires_at
        self._revoked_at = revoked_at

    @classmethod
    def create(
        cls, user_id: Identity, token_hash: str, expires_at: datetime
    ) -> AuthenticationSession:
        """Create an active authentication session."""
        return cls(
            Identity.new(), user_id, token_hash, SessionStatus.ACTIVE, datetime.now(UTC), expires_at
        )

    @property
    def user_id(self) -> Identity:
        """Return session owner identity."""
        return self._user_id

    @property
    def token_hash(self) -> str:
        """Return hashed access token."""
        return self._token_hash

    @property
    def status(self) -> SessionStatus:
        """Return session status."""
        return self._status

    @property
    def created_at(self) -> datetime:
        """Return creation timestamp."""
        return self._created_at

    @property
    def expires_at(self) -> datetime:
        """Return expiration timestamp."""
        return self._expires_at

    @property
    def revoked_at(self) -> datetime | None:
        """Return revocation timestamp."""
        return self._revoked_at

    @property
    def active(self) -> bool:
        """Return whether the session is active and not expired."""
        return self._status == SessionStatus.ACTIVE and self._expires_at > datetime.now(UTC)

    def revoke(self) -> None:
        """Revoke the session."""
        self._status = SessionStatus.REVOKED
        self._revoked_at = datetime.now(UTC)

    def expire(self) -> None:
        """Mark the session as expired."""
        self._status = SessionStatus.EXPIRED

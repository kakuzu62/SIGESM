from __future__ import annotations

from datetime import UTC, datetime

from domain.identity.value_objects import SessionStatus
from shared.kernel.entity import Entity
from shared.kernel.identity import Identity


class UserSession(Entity[Identity]):
    """User authentication session."""

    __slots__ = ("_user_id", "_status", "_created_at", "_expires_at", "_ended_at")

    def __init__(
        self,
        entity_id: Identity,
        user_id: Identity,
        status: SessionStatus,
        created_at: datetime,
        expires_at: datetime,
        ended_at: datetime | None = None,
    ) -> None:
        super().__init__(entity_id)
        self._user_id = user_id
        self._status = status
        self._created_at = created_at
        self._expires_at = expires_at
        self._ended_at = ended_at

    @classmethod
    def create(cls, user_id: Identity, expires_at: datetime) -> UserSession:
        """Create an active user session."""
        return cls(Identity.new(), user_id, SessionStatus.ACTIVE, datetime.now(UTC), expires_at)

    @property
    def user_id(self) -> Identity:
        """Return session owner identity."""
        return self._user_id

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
    def ended_at(self) -> datetime | None:
        """Return end timestamp when closed."""
        return self._ended_at

    def revoke(self) -> None:
        """Revoke the session."""
        self._status = SessionStatus.REVOKED
        self._ended_at = datetime.now(UTC)

    def expire(self) -> None:
        """Mark the session as expired."""
        self._status = SessionStatus.EXPIRED
        self._ended_at = datetime.now(UTC)

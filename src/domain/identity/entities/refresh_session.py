from __future__ import annotations

from datetime import UTC, datetime

from shared.kernel.entity import Entity
from shared.kernel.identity import Identity


class RefreshSession(Entity[Identity]):
    """Refresh session persisted with a hashed refresh token."""

    __slots__ = (
        "_user_id",
        "_session_id",
        "_token_hash",
        "_created_at",
        "_expires_at",
        "_revoked_at",
    )

    def __init__(
        self,
        entity_id: Identity,
        user_id: Identity,
        session_id: Identity,
        token_hash: str,
        created_at: datetime,
        expires_at: datetime,
        revoked_at: datetime | None = None,
    ) -> None:
        super().__init__(entity_id)
        self._user_id = user_id
        self._session_id = session_id
        self._token_hash = token_hash
        self._created_at = created_at
        self._expires_at = expires_at
        self._revoked_at = revoked_at

    @classmethod
    def create(
        cls,
        user_id: Identity,
        session_id: Identity,
        token_hash: str,
        expires_at: datetime,
    ) -> RefreshSession:
        """Create an active refresh session."""
        return cls(Identity.new(), user_id, session_id, token_hash, datetime.now(UTC), expires_at)

    @property
    def user_id(self) -> Identity:
        """Return refresh owner identity."""
        return self._user_id

    @property
    def session_id(self) -> Identity:
        """Return linked authentication session identity."""
        return self._session_id

    @property
    def token_hash(self) -> str:
        """Return hashed refresh token."""
        return self._token_hash

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
        """Return whether refresh session can still be used."""
        return self._revoked_at is None and self._expires_at > datetime.now(UTC)

    def revoke(self) -> None:
        """Revoke the refresh session."""
        self._revoked_at = datetime.now(UTC)

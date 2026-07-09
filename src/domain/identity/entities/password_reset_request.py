from __future__ import annotations

from datetime import UTC, datetime

from shared.kernel.entity import Entity
from shared.kernel.identity import Identity


class PasswordResetRequest(Entity[Identity]):
    """Password reset request stored with a hashed reset token."""

    __slots__ = ("_user_id", "_token_hash", "_created_at", "_expires_at", "_used_at")

    def __init__(
        self,
        entity_id: Identity,
        user_id: Identity,
        token_hash: str,
        created_at: datetime,
        expires_at: datetime,
        used_at: datetime | None = None,
    ) -> None:
        super().__init__(entity_id)
        self._user_id = user_id
        self._token_hash = token_hash
        self._created_at = created_at
        self._expires_at = expires_at
        self._used_at = used_at

    @classmethod
    def create(
        cls, user_id: Identity, token_hash: str, expires_at: datetime
    ) -> PasswordResetRequest:
        """Create a password reset request."""
        return cls(Identity.new(), user_id, token_hash, datetime.now(UTC), expires_at)

    @property
    def user_id(self) -> Identity:
        """Return requester identity."""
        return self._user_id

    @property
    def token_hash(self) -> str:
        """Return hashed reset token."""
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
    def used_at(self) -> datetime | None:
        """Return usage timestamp."""
        return self._used_at

    @property
    def active(self) -> bool:
        """Return whether the reset request can still be used."""
        return self._used_at is None and self._expires_at > datetime.now(UTC)

    def mark_used(self) -> None:
        """Mark the reset request as used."""
        self._used_at = datetime.now(UTC)

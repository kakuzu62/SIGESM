from __future__ import annotations

from argon2 import PasswordHasher
from argon2.exceptions import InvalidHashError, VerificationError, VerifyMismatchError

from domain.identity.policies import PasswordPolicy
from domain.identity.value_objects import PasswordHash


class PasswordService:
    """Service responsible for Argon2id password hashing and verification."""

    def __init__(
        self,
        policy: PasswordPolicy | None = None,
        password_hasher: PasswordHasher | None = None,
    ) -> None:
        self._policy = policy or PasswordPolicy()
        self._password_hasher = password_hasher or PasswordHasher()

    def hash_password(self, raw_password: str) -> PasswordHash:
        """Validate and hash a raw password."""
        self._policy.validate(raw_password)
        return PasswordHash(self._password_hasher.hash(raw_password))

    def verify(self, raw_password: str, password_hash: PasswordHash) -> bool:
        """Return whether a raw password matches a stored hash."""
        try:
            return self._password_hasher.verify(password_hash.value, raw_password)
        except (InvalidHashError, VerificationError, VerifyMismatchError):
            return False

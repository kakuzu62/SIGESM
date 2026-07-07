from __future__ import annotations

import base64
import hashlib
import hmac
import secrets

from domain.identity.policies import PasswordPolicy
from domain.identity.value_objects import PasswordHash


class PasswordService:
    """Service responsible for password hashing and verification."""

    _algorithm = "pbkdf2_sha256"
    _iterations = 600_000
    _salt_size = 16

    def __init__(self, policy: PasswordPolicy | None = None) -> None:
        self._policy = policy or PasswordPolicy()

    def hash_password(self, raw_password: str) -> PasswordHash:
        """Validate and hash a raw password."""
        self._policy.validate(raw_password)
        salt = secrets.token_bytes(self._salt_size)
        digest = hashlib.pbkdf2_hmac(
            "sha256",
            raw_password.encode("utf-8"),
            salt,
            self._iterations,
        )
        encoded_salt = base64.b64encode(salt).decode("ascii")
        encoded_digest = base64.b64encode(digest).decode("ascii")
        return PasswordHash(f"{self._algorithm}${self._iterations}${encoded_salt}${encoded_digest}")

    def verify(self, raw_password: str, password_hash: PasswordHash) -> bool:
        """Return whether a raw password matches a stored hash."""
        algorithm, iterations, encoded_salt, encoded_digest = password_hash.value.split("$")
        if algorithm != self._algorithm:
            return False

        salt = base64.b64decode(encoded_salt.encode("ascii"))
        expected_digest = base64.b64decode(encoded_digest.encode("ascii"))
        actual_digest = hashlib.pbkdf2_hmac(
            "sha256",
            raw_password.encode("utf-8"),
            salt,
            int(iterations),
        )
        return hmac.compare_digest(actual_digest, expected_digest)

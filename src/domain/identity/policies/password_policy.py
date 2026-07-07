from __future__ import annotations

import re

from domain.identity.exceptions import InvalidPasswordException


class PasswordPolicy:
    """Minimum password policy for SIGESM users."""

    def validate(self, password: str) -> None:
        """Validate a raw password against the active policy."""
        if len(password) < 8:
            raise InvalidPasswordException("Password must contain at least 8 characters.")
        if not re.search(r"[A-Z]", password):
            raise InvalidPasswordException("Password must contain an uppercase letter.")
        if not re.search(r"[a-z]", password):
            raise InvalidPasswordException("Password must contain a lowercase letter.")
        if not re.search(r"\d", password):
            raise InvalidPasswordException("Password must contain a number.")
        if not re.search(r"[^A-Za-z0-9]", password):
            raise InvalidPasswordException("Password must contain a special character.")

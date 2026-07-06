from __future__ import annotations

from core.exceptions.base import SIGESMException


class SecurityException(SIGESMException):
    """Raised when authentication, authorization or security checks fail."""

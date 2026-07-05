from __future__ import annotations

from core.exceptions.base import SIGESMException


class ValidationException(SIGESMException):
    """Raised when input or state validation fails."""

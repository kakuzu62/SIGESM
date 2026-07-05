from __future__ import annotations

from core.exceptions.base import SIGESMException


class DomainException(SIGESMException):
    """Raised when a domain invariant or business rule is violated."""

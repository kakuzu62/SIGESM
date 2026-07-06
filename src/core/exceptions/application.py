from __future__ import annotations

from core.exceptions.base import SIGESMException


class ApplicationException(SIGESMException):
    """Raised by application services and use cases."""

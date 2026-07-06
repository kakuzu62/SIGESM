from __future__ import annotations

from core.exceptions.base import SIGESMException


class InfrastructureException(SIGESMException):
    """Raised by infrastructure adapters and external integrations."""

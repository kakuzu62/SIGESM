from __future__ import annotations

from core.exceptions.infrastructure import InfrastructureException


class DatabaseException(InfrastructureException):
    """Raised when persistence infrastructure cannot complete an operation."""

from __future__ import annotations

from core.exceptions.infrastructure import InfrastructureException


class ConfigurationException(InfrastructureException):
    """Raised when application configuration is invalid or incomplete."""

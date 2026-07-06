"""Application exceptions package."""

from core.exceptions.application import ApplicationException
from core.exceptions.base import SIGESMException
from core.exceptions.configuration import ConfigurationException
from core.exceptions.database import DatabaseException
from core.exceptions.domain import DomainException
from core.exceptions.infrastructure import InfrastructureException
from core.exceptions.security import SecurityException
from core.exceptions.validation import ValidationException

__all__ = [
    "ApplicationException",
    "ConfigurationException",
    "DatabaseException",
    "DomainException",
    "InfrastructureException",
    "SecurityException",
    "SIGESMException",
    "ValidationException",
]

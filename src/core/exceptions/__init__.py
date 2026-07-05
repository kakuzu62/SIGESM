"""Application exceptions package."""

from core.exceptions.base import SIGESMException
from core.exceptions.configuration import ConfigurationException
from core.exceptions.database import DatabaseException
from core.exceptions.domain import DomainException
from core.exceptions.validation import ValidationException

__all__ = [
    "ConfigurationException",
    "DatabaseException",
    "DomainException",
    "SIGESMException",
    "ValidationException",
]

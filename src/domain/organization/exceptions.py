from __future__ import annotations

from core.exceptions.domain import DomainException
from core.exceptions.validation import ValidationException


class OrganizationDomainException(DomainException):
    """Raised when an organization domain invariant is violated."""


class InvalidOrganizationCodeException(ValidationException):
    """Raised when an organization code is invalid."""


class InvalidOrganizationNameException(ValidationException):
    """Raised when an organization name is invalid."""


class InvalidAbbreviationException(ValidationException):
    """Raised when an organization abbreviation is invalid."""


class InvalidLocationException(ValidationException):
    """Raised when an organization location value is invalid."""

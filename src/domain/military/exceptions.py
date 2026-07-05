from __future__ import annotations

from core.exceptions.domain import DomainException
from core.exceptions.validation import ValidationException


class MilitaryDomainException(DomainException):
    """Raised when a military domain invariant is violated."""


class InvalidCPFException(ValidationException):
    """Raised when a CPF value is not valid."""


class InvalidMilitaryIdException(ValidationException):
    """Raised when a military identifier is not valid."""


class InvalidFullNameException(ValidationException):
    """Raised when a full name does not satisfy military domain rules."""


class InvalidPhoneException(ValidationException):
    """Raised when a Brazilian phone number is not valid."""


class InvalidRankException(ValidationException):
    """Raised when a military rank is not supported."""

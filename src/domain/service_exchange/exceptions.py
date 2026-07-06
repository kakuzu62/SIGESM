from __future__ import annotations

from core.exceptions.domain import DomainException
from core.exceptions.validation import ValidationException


class ServiceExchangeDomainException(DomainException):
    """Raised when a service exchange domain invariant is violated."""


class InvalidExchangeReasonException(ValidationException):
    """Raised when an exchange reason is invalid."""


class InvalidExchangeOperationException(ServiceExchangeDomainException):
    """Raised when an exchange operation is not allowed."""

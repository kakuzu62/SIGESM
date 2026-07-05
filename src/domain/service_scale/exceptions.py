from __future__ import annotations

from core.exceptions.domain import DomainException
from core.exceptions.validation import ValidationException


class ServiceScaleDomainException(DomainException):
    """Raised when a service scale domain invariant is violated."""


class InvalidScaleTypeException(ValidationException):
    """Raised when a service scale type is invalid."""


class InvalidServiceDateException(ValidationException):
    """Raised when a service date is invalid."""


class InvalidRestPeriodException(ValidationException):
    """Raised when a rest period is invalid."""


class InvalidServiceRoleException(ValidationException):
    """Raised when a service role is invalid."""


class InvalidAssignmentOperationException(ServiceScaleDomainException):
    """Raised when an assignment operation is not allowed."""

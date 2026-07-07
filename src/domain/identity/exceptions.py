from __future__ import annotations

from core.exceptions.domain import DomainException
from core.exceptions.validation import ValidationException


class IdentityDomainException(DomainException):
    """Raised when an identity domain invariant is violated."""


class InvalidUsernameException(ValidationException):
    """Raised when a username is invalid."""


class InvalidEmailException(ValidationException):
    """Raised when an email address is invalid."""


class InvalidPasswordHashException(ValidationException):
    """Raised when a password hash is invalid."""


class InvalidPermissionCodeException(ValidationException):
    """Raised when a permission code is invalid."""


class InvalidPasswordException(ValidationException):
    """Raised when a password does not satisfy the active policy."""

from __future__ import annotations

from collections.abc import Sized
from decimal import Decimal
from typing import TypeVar

from core.exceptions.validation import ValidationException

T = TypeVar("T")
Numeric = int | float | Decimal


class Guard:
    """Common guard clauses used to enforce domain preconditions."""

    @staticmethod
    def against_none(value: T | None, field: str) -> T:
        """Return value when not None, otherwise raise validation error."""
        if value is None:
            raise ValidationException(f"{field} cannot be none.")

        return value

    @staticmethod
    def against_empty(value: str, field: str) -> str:
        """Return value when it is not empty or whitespace."""
        if not value.strip():
            raise ValidationException(f"{field} cannot be empty.")

        return value

    @staticmethod
    def against_negative(value: Numeric, field: str) -> Numeric:
        """Return value when it is not negative."""
        if value < 0:
            raise ValidationException(f"{field} cannot be negative.")

        return value

    @staticmethod
    def against_zero_or_negative(value: Numeric, field: str) -> Numeric:
        """Return value when it is greater than zero."""
        if value <= 0:
            raise ValidationException(f"{field} must be greater than zero.")

        return value

    @staticmethod
    def against_max_length(value: Sized, max_length: int, field: str) -> Sized:
        """Return value when its length is within the maximum allowed size."""
        if len(value) > max_length:
            raise ValidationException(f"{field} cannot exceed {max_length} characters.")

        return value

    @staticmethod
    def against_min_length(value: Sized, min_length: int, field: str) -> Sized:
        """Return value when its length reaches the minimum required size."""
        if len(value) < min_length:
            raise ValidationException(f"{field} must contain at least {min_length} characters.")

        return value

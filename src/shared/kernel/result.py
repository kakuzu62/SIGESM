from __future__ import annotations

from typing import Generic, TypeVar, cast

from core.exceptions.validation import ValidationException

T = TypeVar("T")
_MISSING = object()


class Result(Generic[T]):
    """Generic result type for explicit success and failure flows."""

    __slots__ = ("_value", "_error")

    def __init__(self, value: T | object = _MISSING, error: str | None = None) -> None:
        self._value = value
        self._error = error

    @classmethod
    def success(cls, value: T) -> Result[T]:
        """Create a successful result."""
        return cls(value=value)

    @classmethod
    def failure(cls, error: str) -> Result[T]:
        """Create a failed result."""
        if not error:
            raise ValidationException("Failure result requires an error message.")

        return cls(error=error)

    @property
    def is_success(self) -> bool:
        """Return whether this result represents success."""
        return self._error is None

    @property
    def is_failure(self) -> bool:
        """Return whether this result represents failure."""
        return not self.is_success

    @property
    def value(self) -> T:
        """Return the success value or raise when this result is a failure."""
        if self.is_failure:
            raise ValidationException("Cannot access value from a failure result.")

        return cast(T, self._value)

    @property
    def error(self) -> str:
        """Return the failure error or raise when this result is successful."""
        if self.is_success:
            raise ValidationException("Cannot access error from a success result.")

        return cast(str, self._error)

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class NotificationError:
    """Validation error associated with a specific field."""

    field: str
    message: str


class Notification:
    """Collects validation errors without interrupting control flow."""

    def __init__(self) -> None:
        self._errors: list[NotificationError] = []

    def add_error(self, field: str, message: str) -> None:
        """Add a validation error for the given field."""
        self._errors.append(NotificationError(field=field, message=message))

    @property
    def has_errors(self) -> bool:
        """Return whether at least one validation error was collected."""
        return bool(self._errors)

    @property
    def errors(self) -> tuple[NotificationError, ...]:
        """Return all collected validation errors."""
        return tuple(self._errors)

    def errors_for(self, field: str) -> tuple[NotificationError, ...]:
        """Return validation errors associated with one field."""
        return tuple(error for error in self._errors if error.field == field)

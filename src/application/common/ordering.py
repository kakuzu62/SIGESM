from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

from core.exceptions.validation import ValidationException


class SortDirection(StrEnum):
    """Supported sort directions."""

    ASC = "asc"
    DESC = "desc"


@dataclass(frozen=True, slots=True)
class Ordering:
    """Ordering expression for application queries."""

    field: str
    direction: SortDirection = SortDirection.ASC

    def __post_init__(self) -> None:
        if not self.field.strip():
            raise ValidationException("Ordering field cannot be empty.")

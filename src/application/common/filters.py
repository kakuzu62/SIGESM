from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from typing import Any

from core.exceptions.validation import ValidationException


class FilterOperator(StrEnum):
    """Supported filter operators for query objects."""

    EQUALS = "eq"
    NOT_EQUALS = "ne"
    GREATER_THAN = "gt"
    GREATER_THAN_OR_EQUAL = "gte"
    LESS_THAN = "lt"
    LESS_THAN_OR_EQUAL = "lte"
    CONTAINS = "contains"
    STARTS_WITH = "starts_with"
    ENDS_WITH = "ends_with"
    IN = "in"


@dataclass(frozen=True, slots=True)
class FilterExpression:
    """Single filter expression used by repositories."""

    field: str
    operator: FilterOperator
    value: Any

    def __post_init__(self) -> None:
        if not self.field.strip():
            raise ValidationException("Filter field cannot be empty.")


@dataclass(frozen=True, slots=True)
class FilterGroup:
    """Collection of filter expressions joined by logical AND."""

    expressions: tuple[FilterExpression, ...]

    @classmethod
    def empty(cls) -> FilterGroup:
        """Return an empty filter group."""
        return cls(expressions=())

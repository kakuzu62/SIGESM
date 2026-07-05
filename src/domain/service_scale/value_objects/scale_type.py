from __future__ import annotations

from enum import StrEnum

from domain.service_scale.exceptions import InvalidScaleTypeException


class ScaleType(StrEnum):
    """Initial supported service scale types."""

    PRETA = "preta"
    VERMELHA = "vermelha"

    @classmethod
    def from_string(cls, value: str) -> ScaleType:
        """Create a scale type from a string value."""
        normalized = value.strip().lower()
        for scale_type in cls:
            if scale_type.value == normalized:
                return scale_type
        raise InvalidScaleTypeException(f"Unsupported scale type: {value}.")

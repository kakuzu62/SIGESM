from __future__ import annotations

from collections.abc import Hashable
import re

from domain.organization.exceptions import InvalidOrganizationNameException
from shared.kernel.value_object import ValueObject


class OrganizationName(ValueObject):
    """Official organization name."""

    __slots__ = ("_value",)
    _value: str

    def __init__(self, value: str) -> None:
        normalized = re.sub(r"\s+", " ", value).strip()
        if len(normalized) < 3 or len(normalized) > 150:
            raise InvalidOrganizationNameException("Organization name must have 3 to 150 characters.")

        object.__setattr__(self, "_value", normalized)
        super().__init__()

    @property
    def value(self) -> str:
        """Return the normalized organization name."""
        return self._value

    @property
    def equality_components(self) -> tuple[Hashable, ...]:
        """Return values that define equality."""
        return (self._value.casefold(),)

    def __str__(self) -> str:
        return self._value

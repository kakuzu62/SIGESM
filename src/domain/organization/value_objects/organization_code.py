from __future__ import annotations

from collections.abc import Hashable
import re

from domain.organization.exceptions import InvalidOrganizationCodeException
from shared.kernel.value_object import ValueObject


class OrganizationCode(ValueObject):
    """Normalized organization code used as a business identifier."""

    __slots__ = ("_value",)
    _value: str

    def __init__(self, value: str) -> None:
        normalized = re.sub(r"\s+", "", value).upper()
        if not normalized or not re.fullmatch(r"[A-Z0-9\-]{2,20}", normalized):
            raise InvalidOrganizationCodeException("Organization code must have 2 to 20 letters, digits or hyphens.")

        object.__setattr__(self, "_value", normalized)
        super().__init__()

    @property
    def value(self) -> str:
        """Return the normalized organization code."""
        return self._value

    @property
    def equality_components(self) -> tuple[Hashable, ...]:
        """Return values that define equality."""
        return (self._value,)

    def __str__(self) -> str:
        return self._value

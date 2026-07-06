from __future__ import annotations

from collections.abc import Hashable

from domain.organization.exceptions import InvalidLocationException
from shared.kernel.value_object import ValueObject


class State(ValueObject):
    """Brazilian state abbreviation."""

    __slots__ = ("_value",)
    _value: str

    _VALID_STATES = {
        "AC",
        "AL",
        "AP",
        "AM",
        "BA",
        "CE",
        "DF",
        "ES",
        "GO",
        "MA",
        "MT",
        "MS",
        "MG",
        "PA",
        "PB",
        "PR",
        "PE",
        "PI",
        "RJ",
        "RN",
        "RS",
        "RO",
        "RR",
        "SC",
        "SP",
        "SE",
        "TO",
    }

    def __init__(self, value: str) -> None:
        normalized = value.strip().upper()
        if normalized not in self._VALID_STATES:
            raise InvalidLocationException("State must be a valid Brazilian UF abbreviation.")

        object.__setattr__(self, "_value", normalized)
        super().__init__()

    @property
    def value(self) -> str:
        """Return the normalized state abbreviation."""
        return self._value

    @property
    def equality_components(self) -> tuple[Hashable, ...]:
        """Return values that define equality."""
        return (self._value,)

    def __str__(self) -> str:
        return self._value

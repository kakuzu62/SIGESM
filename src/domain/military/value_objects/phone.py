from __future__ import annotations

from collections.abc import Hashable
import re

from domain.military.exceptions import InvalidPhoneException
from shared.kernel.value_object import ValueObject


class Phone(ValueObject):
    """Brazilian phone number normalized to country code, area code and number."""

    __slots__ = ("_value",)
    _value: str

    def __init__(self, value: str) -> None:
        digits = re.sub(r"\D", "", value)
        normalized = self._normalize(digits)

        object.__setattr__(self, "_value", normalized)
        super().__init__()

    @property
    def value(self) -> str:
        """Return phone in E.164-like Brazilian format."""
        return self._value

    @property
    def equality_components(self) -> tuple[Hashable, ...]:
        """Return values that define equality."""
        return (self._value,)

    def __str__(self) -> str:
        return self._value

    @staticmethod
    def _normalize(digits: str) -> str:
        if len(digits) in {10, 11}:
            digits = f"55{digits}"

        if len(digits) not in {12, 13} or not digits.startswith("55"):
            raise InvalidPhoneException("Phone must be a valid Brazilian number.")

        area_code = digits[2:4]
        subscriber_number = digits[4:]
        if area_code == "00" or subscriber_number.startswith("0"):
            raise InvalidPhoneException("Phone must contain a valid area code and subscriber number.")

        return f"+{digits}"

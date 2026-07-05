from __future__ import annotations

from collections.abc import Hashable
import re

from domain.military.exceptions import InvalidCPFException
from shared.kernel.value_object import ValueObject


class CPF(ValueObject):
    """Brazilian CPF value object with official check digit validation."""

    __slots__ = ("_value",)
    _value: str

    def __init__(self, value: str) -> None:
        digits = re.sub(r"\D", "", value)
        if not self._is_valid(digits):
            raise InvalidCPFException("CPF is not valid.")

        object.__setattr__(self, "_value", digits)
        super().__init__()

    @property
    def value(self) -> str:
        """Return CPF as eleven digits."""
        return self._value

    @property
    def formatted(self) -> str:
        """Return CPF formatted with Brazilian punctuation."""
        return f"{self._value[:3]}.{self._value[3:6]}.{self._value[6:9]}-{self._value[9:]}"

    @property
    def equality_components(self) -> tuple[Hashable, ...]:
        """Return values that define equality."""
        return (self._value,)

    def __str__(self) -> str:
        return self.formatted

    @classmethod
    def _is_valid(cls, digits: str) -> bool:
        """Validate CPF check digits."""
        if len(digits) != 11 or len(set(digits)) == 1:
            return False

        first_digit = cls._calculate_digit(digits[:9], 10)
        second_digit = cls._calculate_digit(digits[:10], 11)
        return digits[-2:] == f"{first_digit}{second_digit}"

    @staticmethod
    def _calculate_digit(base_digits: str, initial_weight: int) -> int:
        total = sum(int(digit) * weight for digit, weight in zip(base_digits, range(initial_weight, 1, -1)))
        remainder = (total * 10) % 11
        return 0 if remainder == 10 else remainder

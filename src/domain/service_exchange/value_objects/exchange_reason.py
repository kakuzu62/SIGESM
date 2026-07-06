from __future__ import annotations

from collections.abc import Hashable
import re

from domain.service_exchange.exceptions import InvalidExchangeReasonException
from shared.kernel.value_object import ValueObject


class ExchangeReason(ValueObject):
    """Auditable reason attached to service exchange decisions."""

    __slots__ = ("_value",)
    _value: str

    def __init__(self, value: str) -> None:
        normalized = re.sub(r"\s+", " ", value).strip()
        if len(normalized) < 5 or len(normalized) > 250:
            raise InvalidExchangeReasonException("Exchange reason must have 5 to 250 characters.")
        object.__setattr__(self, "_value", normalized)
        super().__init__()

    @property
    def value(self) -> str:
        """Return normalized exchange reason."""
        return self._value

    @property
    def equality_components(self) -> tuple[Hashable, ...]:
        """Return values that define equality."""
        return (self._value.casefold(),)

    def __str__(self) -> str:
        return self._value

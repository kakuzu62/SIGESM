from __future__ import annotations

from collections.abc import Hashable
from functools import total_ordering

from domain.military.exceptions import InvalidRankException
from shared.kernel.value_object import ValueObject


@total_ordering
class Rank(ValueObject):
    """Military rank value object with hierarchical ordering."""

    __slots__ = ("_value", "_level")
    _value: str
    _level: int

    _HIERARCHY: tuple[str, ...] = (
        "SOLDADO",
        "CABO",
        "3 SARGENTO",
        "2 SARGENTO",
        "1 SARGENTO",
        "SUBTENENTE",
        "ASPIRANTE",
        "2 TENENTE",
        "1 TENENTE",
        "CAPITAO",
        "MAJOR",
        "TENENTE CORONEL",
        "CORONEL",
        "GENERAL DE BRIGADA",
        "GENERAL DE DIVISAO",
        "GENERAL DE EXERCITO",
    )

    _ALIASES: dict[str, str] = {
        "SD": "SOLDADO",
        "CB": "CABO",
        "3SGT": "3 SARGENTO",
        "3 SGT": "3 SARGENTO",
        "2SGT": "2 SARGENTO",
        "2 SGT": "2 SARGENTO",
        "1SGT": "1 SARGENTO",
        "1 SGT": "1 SARGENTO",
        "ST": "SUBTENENTE",
        "ASP": "ASPIRANTE",
        "2TEN": "2 TENENTE",
        "1TEN": "1 TENENTE",
        "CAP": "CAPITAO",
        "TC": "TENENTE CORONEL",
    }

    def __init__(self, value: str) -> None:
        normalized = " ".join(value.strip().upper().replace("º", "").replace(".", "").split())
        normalized = self._ALIASES.get(normalized, normalized)
        if normalized not in self._HIERARCHY:
            raise InvalidRankException(f"Unsupported military rank: {value}.")

        object.__setattr__(self, "_value", normalized)
        object.__setattr__(self, "_level", self._HIERARCHY.index(normalized))
        super().__init__()

    @property
    def value(self) -> str:
        """Return normalized rank name."""
        return self._value

    @property
    def level(self) -> int:
        """Return numeric hierarchy level."""
        return self._level

    @property
    def equality_components(self) -> tuple[Hashable, ...]:
        """Return values that define equality."""
        return (self._value,)

    def __lt__(self, other: object) -> bool:
        if not isinstance(other, Rank):
            return NotImplemented

        return self.level < other.level

    def __str__(self) -> str:
        return self._value

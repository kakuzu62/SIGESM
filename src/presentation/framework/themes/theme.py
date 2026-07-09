from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum


class ThemeMode(StrEnum):
    """Supported desktop theme modes."""

    LIGHT = "LIGHT"
    DARK = "DARK"


@dataclass(frozen=True, slots=True)
class ThemePalette:
    """Named palette used by reusable desktop components."""

    mode: ThemeMode
    background: str
    surface: str
    text: str
    primary: str
    danger: str

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from pathlib import Path


class ThemeMode(StrEnum):
    """Supported desktop theme modes."""

    LIGHT = "LIGHT"
    DARK = "DARK"
    HIGH_CONTRAST = "HIGH_CONTRAST"


@dataclass(frozen=True, slots=True)
class Theme:
    """Desktop theme descriptor."""

    name: str
    display_name: str
    qss_path: Path


@dataclass(frozen=True, slots=True)
class ThemePalette:
    """Named palette used by reusable desktop components."""

    mode: ThemeMode
    background: str
    surface: str
    text: str
    primary: str
    danger: str

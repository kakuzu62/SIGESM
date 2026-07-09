from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class UiCommand:
    """Reusable UI command descriptor."""

    name: str
    label: str
    execute: Callable[[], None]
    enabled: bool = True

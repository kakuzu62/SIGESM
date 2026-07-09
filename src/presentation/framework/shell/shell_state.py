from __future__ import annotations

from dataclasses import dataclass

from presentation.framework.themes import ThemeMode


@dataclass(frozen=True, slots=True)
class ShellState:
    """Serializable state of the desktop shell."""

    title: str
    theme: ThemeMode
    current_route: str | None = None

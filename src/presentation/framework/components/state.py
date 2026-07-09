from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ComponentState:
    """Reusable state flags for UI components."""

    visible: bool = True
    enabled: bool = True
    loading: bool = False
    error: str | None = None

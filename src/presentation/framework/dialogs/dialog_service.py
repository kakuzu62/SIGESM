from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class DialogRequest:
    """Request descriptor for a UI dialog."""

    title: str
    message: str
    severity: str = "info"


@dataclass(frozen=True, slots=True)
class DialogResult:
    """Result returned by a UI dialog."""

    accepted: bool
    value: str | None = None

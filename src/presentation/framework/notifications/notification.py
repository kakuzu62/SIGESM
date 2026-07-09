from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Notification:
    """User-facing desktop notification."""

    title: str
    message: str
    severity: str = "info"

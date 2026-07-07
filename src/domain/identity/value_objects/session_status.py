from __future__ import annotations

from enum import StrEnum


class SessionStatus(StrEnum):
    """Supported user session states."""

    ACTIVE = "ACTIVE"
    EXPIRED = "EXPIRED"
    REVOKED = "REVOKED"

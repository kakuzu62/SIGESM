from __future__ import annotations

from enum import StrEnum


class MilitaryStatus(StrEnum):
    """Operational status for a military person."""

    ACTIVE = "active"
    INACTIVE = "inactive"
    ON_LEAVE = "on_leave"
    RESTRICTED = "restricted"

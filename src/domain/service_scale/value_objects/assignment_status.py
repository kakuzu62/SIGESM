from __future__ import annotations

from enum import StrEnum


class AssignmentStatus(StrEnum):
    """Status of a service assignment."""

    SCHEDULED = "scheduled"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    REPLACED = "replaced"

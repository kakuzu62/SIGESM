from __future__ import annotations

from enum import StrEnum


class EligibilityReason(StrEnum):
    """Reasons that explain why a military person is not eligible for service."""

    INSUFFICIENT_REST = "insufficient_rest"
    MILITARY_INACTIVE = "military_inactive"
    ON_LEAVE = "on_leave"
    RESTRICTED = "restricted"
    ROLE_NOT_ALLOWED = "role_not_allowed"
    SCALE_NOT_ALLOWED = "scale_not_allowed"
    SERVICE_CONFLICT = "service_conflict"
    ALREADY_ASSIGNED = "already_assigned"
    MANUAL_BLOCK = "manual_block"
    UNKNOWN = "unknown"

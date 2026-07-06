from __future__ import annotations

from enum import StrEnum


class ExchangeStatus(StrEnum):
    """Lifecycle status for official swaps and service sales."""

    REQUESTED = "requested"
    APPROVED = "approved"
    REJECTED = "rejected"

from __future__ import annotations

from enum import StrEnum


class ExchangeType(StrEnum):
    """Type of service exchange operation."""

    OFFICIAL_SWAP = "official_swap"
    SERVICE_SALE = "service_sale"

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ListAvailableRolesQuery:
    """Query for roles available to assign."""

    include_inactive: bool = False

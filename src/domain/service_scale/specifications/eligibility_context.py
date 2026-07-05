from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass

from domain.military.entities import MilitaryPerson
from domain.service_scale.entities import ServiceAssignment, ServiceRole, ServiceScale
from domain.service_scale.value_objects import ServiceDate
from shared.kernel.identity import Identity


@dataclass(frozen=True, slots=True)
class EligibilityContext:
    """Input data evaluated by eligibility specifications."""

    military: MilitaryPerson
    service_scale: ServiceScale
    service_role: ServiceRole
    history: tuple[ServiceAssignment, ...]
    service_date: ServiceDate
    allowed_role_ids_by_military: Mapping[Identity, frozenset[Identity]]
    allowed_scale_ids_by_military: Mapping[Identity, frozenset[Identity]]
    manually_blocked_military_ids: frozenset[Identity]
    allow_one_by_one_exception: bool

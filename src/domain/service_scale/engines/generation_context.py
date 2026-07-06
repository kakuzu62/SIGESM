from __future__ import annotations

from dataclasses import dataclass
from types import MappingProxyType
from typing import TYPE_CHECKING, Any, Mapping

from domain.service_scale.value_objects import ScaleType, ServiceDate
from shared.kernel.identity import Identity

if TYPE_CHECKING:
    from domain.military.entities import MilitaryPerson
    from domain.service_scale.entities import ServiceAssignment, ServiceRole, ServiceScale


@dataclass(frozen=True, slots=True)
class GenerationContext:
    """Immutable input data required to generate a service scale."""

    service_date: ServiceDate
    scale_type: ScaleType
    service_scale: ServiceScale
    service_role: ServiceRole
    eligible_military: tuple[MilitaryPerson, ...]
    blocked_military_ids: frozenset[Identity]
    history: tuple[ServiceAssignment, ...]
    restrictions: Mapping[str, Any]
    parameters: Mapping[str, Any]

    @classmethod
    def create(
        cls,
        service_date: ServiceDate,
        scale_type: ScaleType,
        service_scale: ServiceScale,
        service_role: ServiceRole,
        eligible_military: tuple[MilitaryPerson, ...],
        blocked_military_ids: frozenset[Identity] = frozenset(),
        history: tuple[ServiceAssignment, ...] = (),
        restrictions: Mapping[str, Any] | None = None,
        parameters: Mapping[str, Any] | None = None,
    ) -> GenerationContext:
        """Create an immutable generation context."""
        return cls(
            service_date=service_date,
            scale_type=scale_type,
            service_scale=service_scale,
            service_role=service_role,
            eligible_military=eligible_military,
            blocked_military_ids=blocked_military_ids,
            history=history,
            restrictions=MappingProxyType(dict(restrictions or {})),
            parameters=MappingProxyType(dict(parameters or {})),
        )

    @property
    def selection_limit(self) -> int:
        """Return how many military persons should be selected."""
        value = self.parameters.get("selection_limit", 1)
        return int(value)

    @property
    def allow_one_by_one_exception(self) -> bool:
        """Return whether controlled 1x1 rest exception is enabled."""
        return bool(self.parameters.get("allow_one_by_one_exception", False))

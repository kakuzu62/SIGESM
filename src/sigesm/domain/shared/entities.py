from __future__ import annotations

from dataclasses import dataclass, field
from typing import Generic, TypeVar

from sigesm.domain.shared.events import DomainEvent

EntityId = TypeVar("EntityId")


@dataclass(kw_only=True)
class Entity(Generic[EntityId]):
    id: EntityId
    _domain_events: list[DomainEvent] = field(default_factory=list, init=False, repr=False)

    def collect_events(self) -> tuple[DomainEvent, ...]:
        events = tuple(self._domain_events)
        self._domain_events.clear()
        return events

    def register_event(self, event: DomainEvent) -> None:
        self._domain_events.append(event)

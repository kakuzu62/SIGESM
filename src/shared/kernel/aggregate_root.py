from __future__ import annotations

from typing import Generic, TypeVar

from shared.kernel.domain_event import DomainEvent
from shared.kernel.entity import Entity

IdentityT = TypeVar("IdentityT")


class AggregateRoot(Entity[IdentityT], Generic[IdentityT]):
    """Base entity that records domain events raised by an aggregate."""

    __slots__ = ("_domain_events",)

    def __init__(self, entity_id: IdentityT) -> None:
        super().__init__(entity_id)
        self._domain_events: list[DomainEvent] = []

    def add_domain_event(self, event: DomainEvent) -> None:
        """Record a domain event to be dispatched after persistence."""
        self._domain_events.append(event)

    def clear_domain_events(self) -> None:
        """Remove all pending domain events from the aggregate."""
        self._domain_events.clear()

    def pull_domain_events(self) -> tuple[DomainEvent, ...]:
        """Return pending domain events and clear the internal collection."""
        events = tuple(self._domain_events)
        self.clear_domain_events()
        return events

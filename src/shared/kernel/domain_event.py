from __future__ import annotations

from abc import ABC
from datetime import UTC, datetime
from uuid import UUID, uuid4


class DomainEvent(ABC):
    """Base class for immutable domain events."""

    __slots__ = ("_event_id", "_occurred_on")

    def __init__(self) -> None:
        self._event_id = uuid4()
        self._occurred_on = datetime.now(UTC)

    @property
    def event_id(self) -> UUID:
        """Return this event unique identifier."""
        return self._event_id

    @property
    def occurred_on(self) -> datetime:
        """Return when this event occurred."""
        return self._occurred_on

    @property
    def event_name(self) -> str:
        """Return the event name used for logging and dispatching."""
        return type(self).__name__

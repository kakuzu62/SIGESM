from __future__ import annotations

import logging
from collections import defaultdict
from collections.abc import Callable
from typing import TypeVar, cast

from shared.kernel.domain_event import DomainEvent

EventT = TypeVar("EventT", bound=DomainEvent)
logger = logging.getLogger(__name__)


class EventDispatcher:
    """Synchronous in-process dispatcher for domain events."""

    def __init__(self) -> None:
        self._handlers: dict[type[DomainEvent], list[Callable[[DomainEvent], None]]] = defaultdict(
            list
        )

    def register(self, event_type: type[EventT], handler: Callable[[EventT], None]) -> None:
        """Register a handler for a domain event type."""
        self._handlers[event_type].append(cast(Callable[[DomainEvent], None], handler))

    def dispatch(self, event: DomainEvent) -> None:
        """Dispatch an event synchronously to registered handlers."""
        for handler in tuple(self._handlers.get(type(event), ())):
            try:
                handler(event)
            except Exception:
                logger.exception("Erro ao processar evento de dominio %s.", event.event_name)
                raise

    def clear(self) -> None:
        """Remove all registered event handlers."""
        self._handlers.clear()

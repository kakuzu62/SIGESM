"""Shared kernel primitives for domain-driven design."""

from shared.kernel.aggregate_root import AggregateRoot
from shared.kernel.domain_event import DomainEvent
from shared.kernel.entity import Entity
from shared.kernel.event_dispatcher import EventDispatcher
from shared.kernel.guard import Guard
from shared.kernel.identity import Identity
from shared.kernel.notification import Notification, NotificationError
from shared.kernel.result import Result
from shared.kernel.specification import Specification
from shared.kernel.value_object import ValueObject

__all__ = [
    "AggregateRoot",
    "DomainEvent",
    "Entity",
    "EventDispatcher",
    "Guard",
    "Identity",
    "Notification",
    "NotificationError",
    "Result",
    "Specification",
    "ValueObject",
]

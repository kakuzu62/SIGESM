"""Service scale domain events."""

from domain.service_scale.events.service_assignment_cancelled import ServiceAssignmentCancelled
from domain.service_scale.events.service_assignment_created import ServiceAssignmentCreated

__all__ = ["ServiceAssignmentCancelled", "ServiceAssignmentCreated"]

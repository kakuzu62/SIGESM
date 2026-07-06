"""Service scale domain events."""

from domain.service_scale.events.service_assignment_cancelled import ServiceAssignmentCancelled
from domain.service_scale.events.service_assignment_created import ServiceAssignmentCreated
from domain.service_scale.events.military_declared_eligible import MilitaryDeclaredEligible
from domain.service_scale.events.military_declared_ineligible import MilitaryDeclaredIneligible
from domain.service_scale.events.military_selected import MilitarySelected
from domain.service_scale.events.military_skipped import MilitarySkipped
from domain.service_scale.events.scale_generated import ScaleGenerated

__all__ = [
    "MilitaryDeclaredEligible",
    "MilitaryDeclaredIneligible",
    "MilitarySelected",
    "MilitarySkipped",
    "ScaleGenerated",
    "ServiceAssignmentCancelled",
    "ServiceAssignmentCreated",
]

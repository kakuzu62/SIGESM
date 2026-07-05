"""Service scale value objects."""

from domain.service_scale.value_objects.assignment_status import AssignmentStatus
from domain.service_scale.value_objects.rest_period import RestPeriod
from domain.service_scale.value_objects.scale_type import ScaleType
from domain.service_scale.value_objects.service_date import ServiceDate
from domain.service_scale.value_objects.service_role_name import ServiceRoleName

__all__ = ["AssignmentStatus", "RestPeriod", "ScaleType", "ServiceDate", "ServiceRoleName"]

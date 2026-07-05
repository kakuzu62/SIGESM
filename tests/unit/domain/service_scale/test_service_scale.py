from __future__ import annotations

from datetime import UTC, datetime, timedelta

import pytest

from domain.service_scale.entities import ServiceScale
from domain.service_scale.events import ServiceAssignmentCancelled, ServiceAssignmentCreated
from domain.service_scale.exceptions import InvalidAssignmentOperationException
from domain.service_scale.policies import MinimumRestPolicy, TieBreakCandidate, TieBreakPolicy
from domain.service_scale.specifications.military_available_for_scale import (
    MilitaryAvailableForScaleSpecification,
    MilitaryScaleAvailability,
)
from domain.service_scale.specifications.minimum_rest_satisfied import (
    MinimumRestEvaluation,
    MinimumRestSatisfiedSpecification,
)
from domain.service_scale.value_objects import (
    AssignmentStatus,
    RestPeriod,
    ScaleType,
    ServiceDate,
    ServiceRoleName,
)
from shared.kernel.identity import Identity


def _scale(scale_type: ScaleType = ScaleType.PRETA) -> ServiceScale:
    service_scale = ServiceScale.create(scale_type)
    service_scale.add_service_role(ServiceRoleName("Sentinela"))
    return service_scale


def test_create_black_scale() -> None:
    service_scale = ServiceScale.create(ScaleType.PRETA)

    assert service_scale.scale_type == ScaleType.PRETA
    assert service_scale.roles == ()
    assert service_scale.assignments == ()


def test_create_red_scale() -> None:
    service_scale = ServiceScale.create(ScaleType.VERMELHA)

    assert service_scale.scale_type == ScaleType.VERMELHA


def test_standard_minimum_rest_of_78_hours() -> None:
    policy = MinimumRestPolicy()
    specification = MinimumRestSatisfiedSpecification(policy)

    assert specification.is_satisfied_by(MinimumRestEvaluation(RestPeriod(78)))
    assert not specification.is_satisfied_by(MinimumRestEvaluation(RestPeriod(77)))


def test_one_by_one_exception_allowed() -> None:
    policy = MinimumRestPolicy()

    assert policy.is_satisfied(RestPeriod(24), allow_one_by_one_exception=True)


def test_one_by_one_exception_denied() -> None:
    policy = MinimumRestPolicy()

    assert not policy.is_satisfied(RestPeriod(24), allow_one_by_one_exception=False)


def test_create_assignment_emits_event() -> None:
    service_scale = _scale()
    role = service_scale.roles[0]
    military_id = Identity.new()

    assignment = service_scale.create_assignment(
        military_id=military_id,
        service_date=ServiceDate(datetime(2026, 7, 6, tzinfo=UTC).date()),
        role_id=role.id,
    )

    assert assignment.military_id == military_id
    assert assignment.scale_type == ScaleType.PRETA
    assert assignment.status == AssignmentStatus.SCHEDULED
    events = service_scale.pull_domain_events()
    assert len(events) == 1
    assert isinstance(events[0], ServiceAssignmentCreated)
    assert events[0].assignment_id == assignment.id


def test_cancel_assignment_with_reason_emits_event() -> None:
    service_scale = _scale()
    assignment = service_scale.create_assignment(
        military_id=Identity.new(),
        service_date=ServiceDate(datetime(2026, 7, 7, tzinfo=UTC).date()),
        role_id=service_scale.roles[0].id,
    )
    service_scale.pull_domain_events()

    service_scale.cancel_assignment(assignment.id, "Operational adjustment")

    assert assignment.status == AssignmentStatus.CANCELLED
    assert assignment.cancellation_reason == "Operational adjustment"
    events = service_scale.pull_domain_events()
    assert len(events) == 1
    assert isinstance(events[0], ServiceAssignmentCancelled)


def test_cancel_assignment_requires_reason() -> None:
    service_scale = _scale()
    assignment = service_scale.create_assignment(
        military_id=Identity.new(),
        service_date=ServiceDate(datetime(2026, 7, 8, tzinfo=UTC).date()),
        role_id=service_scale.roles[0].id,
    )

    with pytest.raises(InvalidAssignmentOperationException):
        service_scale.cancel_assignment(assignment.id, " ")


def test_complete_assignment() -> None:
    service_scale = _scale()
    assignment = service_scale.create_assignment(
        military_id=Identity.new(),
        service_date=ServiceDate(datetime(2026, 7, 9, tzinfo=UTC).date()),
        role_id=service_scale.roles[0].id,
    )

    service_scale.complete_assignment(assignment.id)

    assert assignment.status == AssignmentStatus.COMPLETED


def test_military_available_for_scale_specification() -> None:
    specification = MilitaryAvailableForScaleSpecification()
    candidate = MilitaryScaleAvailability(
        military_id=Identity.new(),
        rest_period=RestPeriod(78),
        has_conflicting_assignment=False,
    )
    conflicting = MilitaryScaleAvailability(
        military_id=Identity.new(),
        rest_period=RestPeriod(78),
        has_conflicting_assignment=True,
    )

    assert specification.is_satisfied_by(candidate)
    assert not specification.is_satisfied_by(conflicting)


def test_deterministic_tie_break() -> None:
    now = datetime(2026, 7, 5, tzinfo=UTC)
    first = TieBreakCandidate(
        military_id=Identity.new(),
        last_service_at=now - timedelta(days=10),
        total_assignments=2,
        audit_key="B",
    )
    second = TieBreakCandidate(
        military_id=Identity.new(),
        last_service_at=now - timedelta(days=30),
        total_assignments=1,
        audit_key="A",
    )
    third = TieBreakCandidate(
        military_id=Identity.new(),
        last_service_at=now - timedelta(days=40),
        total_assignments=1,
        audit_key="C",
    )

    selected = TieBreakPolicy().choose((first, second, third))

    assert selected == third

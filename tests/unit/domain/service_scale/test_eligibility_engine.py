from __future__ import annotations

from datetime import UTC, datetime

from domain.military.entities import MilitaryPerson
from domain.military.value_objects import CPF, FullName, MilitaryId, MilitaryStatus, Phone, Rank
from domain.service_scale.entities import ServiceAssignment, ServiceRole, ServiceScale
from domain.service_scale.events import MilitaryDeclaredEligible, MilitaryDeclaredIneligible
from domain.service_scale.policies.eligibility_policy import (
    EligibilityPolicy,
    EligibilityPolicyConfiguration,
)
from domain.service_scale.services.eligibility_engine import EligibilityEngine
from domain.service_scale.services.eligibility_reason import EligibilityReason
from domain.service_scale.services.eligibility_result import EligibilityResult
from domain.service_scale.value_objects import ScaleType, ServiceDate, ServiceRoleName
from shared.kernel.identity import Identity


def _military(status: MilitaryStatus = MilitaryStatus.ACTIVE) -> MilitaryPerson:
    now = datetime.now(UTC)
    return MilitaryPerson(
        entity_id=Identity.new(),
        military_id=MilitaryId("EB-ELIG-001"),
        full_name=FullName("Carlos Alberto Silva"),
        cpf=CPF("52998224725"),
        rank=Rank("Cabo"),
        phone=Phone("(11) 98888-7777"),
        status=status,
        created_at=now,
        updated_at=now,
    )


def _scale(scale_type: ScaleType = ScaleType.PRETA) -> tuple[ServiceScale, ServiceRole]:
    service_scale = ServiceScale.create(scale_type)
    role = service_scale.add_service_role(ServiceRoleName("Sentinela"))
    return service_scale, role


def _assignment_for(military: MilitaryPerson, service_date: ServiceDate) -> ServiceAssignment:
    service_scale, role = _scale()
    return service_scale.create_assignment(
        military_id=military.id,
        service_date=service_date,
        role_id=role.id,
    )


def _evaluate(
    military: MilitaryPerson,
    service_scale: ServiceScale,
    role: ServiceRole,
    history: tuple[ServiceAssignment, ...] = (),
    service_date: ServiceDate = ServiceDate(datetime(2026, 7, 10, tzinfo=UTC).date()),
    policy: EligibilityPolicy | None = None,
) -> tuple[EligibilityEngine, EligibilityResult]:
    engine = EligibilityEngine(policy)
    return engine, engine.evaluate(military, service_scale, role, history, service_date)


def test_military_is_eligible() -> None:
    military = _military()
    service_scale, role = _scale()
    engine, result = _evaluate(military, service_scale, role)

    assert result.eligible
    assert result.reasons == ()
    assert isinstance(engine.pull_domain_events()[0], MilitaryDeclaredEligible)


def test_military_without_minimum_rest_is_ineligible() -> None:
    military = _military()
    service_scale, role = _scale()
    previous = _assignment_for(military, ServiceDate(datetime(2026, 7, 8, tzinfo=UTC).date()))

    engine, result = _evaluate(military, service_scale, role, history=(previous,))

    assert not result.eligible
    assert EligibilityReason.INSUFFICIENT_REST in result.reasons
    event = engine.pull_domain_events()[0]
    assert isinstance(event, MilitaryDeclaredIneligible)
    assert EligibilityReason.INSUFFICIENT_REST in event.reasons


def test_military_on_leave_is_ineligible() -> None:
    military = _military(MilitaryStatus.ON_LEAVE)
    service_scale, role = _scale()

    _, result = _evaluate(military, service_scale, role)

    assert EligibilityReason.ON_LEAVE in result.reasons


def test_inactive_military_is_ineligible() -> None:
    military = _military(MilitaryStatus.INACTIVE)
    service_scale, role = _scale()

    _, result = _evaluate(military, service_scale, role)

    assert EligibilityReason.MILITARY_INACTIVE in result.reasons


def test_restricted_military_is_ineligible() -> None:
    military = _military(MilitaryStatus.RESTRICTED)
    service_scale, role = _scale()

    _, result = _evaluate(military, service_scale, role)

    assert EligibilityReason.RESTRICTED in result.reasons


def test_role_incompatibility_is_ineligible() -> None:
    military = _military()
    service_scale, role = _scale()
    policy = EligibilityPolicy(
        configuration=EligibilityPolicyConfiguration(
            allowed_role_ids_by_military={military.id: frozenset()},
            allowed_scale_ids_by_military={},
            manually_blocked_military_ids=frozenset(),
        )
    )

    _, result = _evaluate(military, service_scale, role, policy=policy)

    assert EligibilityReason.ROLE_NOT_ALLOWED in result.reasons


def test_scale_incompatibility_is_ineligible() -> None:
    military = _military()
    service_scale, role = _scale(ScaleType.VERMELHA)
    policy = EligibilityPolicy(
        configuration=EligibilityPolicyConfiguration(
            allowed_role_ids_by_military={},
            allowed_scale_ids_by_military={military.id: frozenset()},
            manually_blocked_military_ids=frozenset(),
        )
    )

    _, result = _evaluate(military, service_scale, role, policy=policy)

    assert EligibilityReason.SCALE_NOT_ALLOWED in result.reasons


def test_multiple_reasons_are_returned_together() -> None:
    military = _military(MilitaryStatus.INACTIVE)
    service_scale, role = _scale()
    previous = _assignment_for(military, ServiceDate(datetime(2026, 7, 8, tzinfo=UTC).date()))
    service_scale.create_assignment(
        military_id=military.id,
        service_date=ServiceDate(datetime(2026, 7, 10, tzinfo=UTC).date()),
        role_id=role.id,
    )
    policy = EligibilityPolicy(
        configuration=EligibilityPolicyConfiguration(
            allowed_role_ids_by_military={military.id: frozenset()},
            allowed_scale_ids_by_military={military.id: frozenset()},
            manually_blocked_military_ids=frozenset((military.id,)),
        )
    )

    _, result = _evaluate(military, service_scale, role, history=(previous,), policy=policy)

    assert result.reasons == (
        EligibilityReason.MILITARY_INACTIVE,
        EligibilityReason.INSUFFICIENT_REST,
        EligibilityReason.ROLE_NOT_ALLOWED,
        EligibilityReason.SCALE_NOT_ALLOWED,
        EligibilityReason.ALREADY_ASSIGNED,
        EligibilityReason.MANUAL_BLOCK,
    )


def test_service_conflict_is_reported_from_history() -> None:
    military = _military()
    service_scale, role = _scale()
    current_date = ServiceDate(datetime(2026, 7, 10, tzinfo=UTC).date())
    conflict = _assignment_for(military, current_date)

    _, result = _evaluate(military, service_scale, role, history=(conflict,), service_date=current_date)

    assert EligibilityReason.SERVICE_CONFLICT in result.reasons

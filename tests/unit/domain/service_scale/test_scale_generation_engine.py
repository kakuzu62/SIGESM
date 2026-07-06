from __future__ import annotations

from datetime import UTC, datetime

from domain.military.entities import MilitaryPerson
from domain.service_scale.entities.service_assignment import ServiceAssignment
from domain.military.value_objects import CPF, FullName, MilitaryId, Phone, Rank
from domain.service_scale.engines.generation_context import GenerationContext
from domain.service_scale.engines.scale_generation_engine import ScaleGenerationEngine
from domain.service_scale.events import MilitarySelected, MilitarySkipped, ScaleGenerated
from domain.service_scale.value_objects import ScaleType, ServiceDate, ServiceRoleName
from shared.kernel.identity import Identity


def _military(number: int) -> MilitaryPerson:
    names = ("Militar Teste Um", "Militar Teste Dois", "Militar Teste Tres")
    return MilitaryPerson.register(
        military_id=MilitaryId(f"EB-{number:03d}"),
        full_name=FullName(names[number - 1]),
        cpf=CPF(("52998224725", "39053344705", "11144477735")[number - 1]),
        rank=Rank("Cabo"),
        phone=Phone("(11) 98888-7777"),
    )


def _context(
    scale_type: ScaleType,
    candidates: tuple[MilitaryPerson, ...],
    service_date: ServiceDate = ServiceDate(datetime(2026, 7, 10, tzinfo=UTC).date()),
    history: tuple[ServiceAssignment, ...] = (),
    parameters: dict[str, object] | None = None,
    restrictions: dict[str, object] | None = None,
    blocked_ids: frozenset[Identity] = frozenset(),
) -> GenerationContext:
    from domain.service_scale.entities import ServiceScale

    scale = ServiceScale.create(scale_type)
    role = scale.add_service_role(ServiceRoleName("Sentinela"))
    return GenerationContext.create(
        service_date=service_date,
        scale_type=scale_type,
        service_scale=scale,
        service_role=role,
        eligible_military=candidates,
        blocked_military_ids=blocked_ids,
        history=history,
        restrictions=restrictions,
        parameters=parameters,
    )


def test_generate_black_scale() -> None:
    first = _military(1)
    second = _military(2)

    result = ScaleGenerationEngine().generate(
        _context(ScaleType.PRETA, (first, second), parameters={"selection_limit": 1})
    )

    assert len(result.selected_military) == 1
    assert result.statistics.analyzed_count == 2
    assert result.statistics.selected_count == 1
    assert any(isinstance(event, ScaleGenerated) for event in result.events)


def test_generate_red_scale() -> None:
    first = _military(1)
    second = _military(2)

    result = ScaleGenerationEngine().generate(
        _context(ScaleType.VERMELHA, (second, first), parameters={"selection_limit": 1})
    )

    assert result.selected_military[0].military_id.value == "EB-001"


def test_generation_respects_78_hours_rest() -> None:
    military = _military(1)
    from domain.service_scale.entities import ServiceScale

    previous_scale = ServiceScale.create(ScaleType.PRETA)
    role = previous_scale.add_service_role(ServiceRoleName("Sentinela"))
    previous = previous_scale.create_assignment(
        military_id=military.id,
        service_date=ServiceDate(datetime(2026, 7, 8, tzinfo=UTC).date()),
        role_id=role.id,
    )

    result = ScaleGenerationEngine().generate(
        _context(ScaleType.PRETA, (military,), history=(previous,))
    )

    assert result.selected_military == ()
    assert result.statistics.skipped_count == 1


def test_generation_allows_one_by_one_exception() -> None:
    military = _military(1)
    from domain.service_scale.entities import ServiceScale

    previous_scale = ServiceScale.create(ScaleType.PRETA)
    role = previous_scale.add_service_role(ServiceRoleName("Sentinela"))
    previous = previous_scale.create_assignment(
        military_id=military.id,
        service_date=ServiceDate(datetime(2026, 7, 8, tzinfo=UTC).date()),
        role_id=role.id,
    )

    result = ScaleGenerationEngine().generate(
        _context(
            ScaleType.PRETA,
            (military,),
            history=(previous,),
            parameters={"allow_one_by_one_exception": True},
        )
    )

    assert result.selected_military == (military,)


def test_generation_selects_multiple_candidates() -> None:
    candidates = (_military(1), _military(2), _military(3))

    result = ScaleGenerationEngine().generate(
        _context(ScaleType.PRETA, candidates, parameters={"selection_limit": 2})
    )

    assert len(result.selected_military) == 2
    assert result.statistics.eligible_count == 3


def test_generation_uses_fairness_for_tie() -> None:
    first = _military(1)
    second = _military(2)
    from domain.service_scale.entities import ServiceScale

    previous_scale = ServiceScale.create(ScaleType.PRETA)
    role = previous_scale.add_service_role(ServiceRoleName("Sentinela"))
    previous = previous_scale.create_assignment(
        military_id=first.id,
        service_date=ServiceDate(datetime(2026, 7, 1, tzinfo=UTC).date()),
        role_id=role.id,
    )

    result = ScaleGenerationEngine().generate(
        _context(ScaleType.PRETA, (first, second), history=(previous,))
    )

    assert result.selected_military == (second,)


def test_generation_integrates_with_eligibility_engine_and_events() -> None:
    first = _military(1)
    second = _military(2)
    context = _context(
        ScaleType.PRETA,
        (first, second),
        restrictions={"allowed_role_ids_by_military": {first.id: frozenset()}},
    )

    result = ScaleGenerationEngine().generate(context)

    assert result.selected_military == (second,)
    assert result.skip_reasons[first.id]
    assert any(isinstance(event, MilitarySkipped) for event in result.events)
    assert any(isinstance(event, MilitarySelected) for event in result.events)


def test_generation_statistics_are_recorded() -> None:
    candidates = (_military(1), _military(2))

    result = ScaleGenerationEngine().generate(_context(ScaleType.PRETA, candidates))

    assert result.generation_id is not None
    assert result.processing_time_seconds >= 0
    assert result.statistics.verification_count == 2
    assert result.statistics.execution_time_seconds >= 0

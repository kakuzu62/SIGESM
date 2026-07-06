from __future__ import annotations

from datetime import UTC, datetime

from domain.military.entities import MilitaryPerson
from domain.military.value_objects import CPF, FullName, MilitaryId, Phone, Rank
from domain.service_exchange.entities import OfficialSwap, ServiceSale
from domain.service_exchange.events import (
    OfficialSwapApproved,
    OfficialSwapRejected,
    ServiceSaleApproved,
    ServiceSaleRejected,
)
from domain.service_exchange.policies import OfficialSwapPolicy, ServiceSalePolicy
from domain.service_exchange.engines import ServiceSaleEngine, SwapValidationEngine
from domain.service_exchange.value_objects import ExchangeReason, ExchangeStatus
from domain.service_scale.entities import ServiceAssignment, ServiceRole, ServiceScale
from domain.service_scale.services.eligibility_reason import EligibilityReason
from domain.service_scale.value_objects import ScaleType, ServiceDate, ServiceRoleName
from shared.kernel.identity import Identity


def _military(number: int) -> MilitaryPerson:
    names = ("Militar Alfa Teste", "Militar Bravo Teste")
    cpfs = ("52998224725", "39053344705")
    return MilitaryPerson.register(
        military_id=MilitaryId(f"EB-SWAP-{number:03d}"),
        full_name=FullName(names[number - 1]),
        cpf=CPF(cpfs[number - 1]),
        rank=Rank("Cabo"),
        phone=Phone("(11) 98888-7777"),
    )


def _scale() -> tuple[ServiceScale, ServiceRole]:
    service_scale = ServiceScale.create(ScaleType.PRETA)
    role = service_scale.add_service_role(ServiceRoleName("Sentinela"))
    return service_scale, role


def _assignment(
    service_scale: ServiceScale,
    role: ServiceRole,
    military: MilitaryPerson,
    year: int,
    month: int,
    day: int,
) -> ServiceAssignment:
    return service_scale.create_assignment(
        military_id=military.id,
        service_date=ServiceDate(datetime(year, month, day, tzinfo=UTC).date()),
        role_id=role.id,
    )


def test_valid_official_swap() -> None:
    first = _military(1)
    second = _military(2)
    service_scale, role = _scale()
    first_assignment = _assignment(service_scale, role, first, 2026, 7, 20)
    second_assignment = _assignment(service_scale, role, second, 2026, 7, 25)
    swap = OfficialSwap.request(first.id, ExchangeReason("Troca operacional planejada"), first_assignment, second_assignment)

    decision = SwapValidationEngine().evaluate(
        swap=swap,
        source_military=first,
        target_military=second,
        service_scale=service_scale,
        source_role=role,
        target_role=role,
        history=(),
        decided_by=Identity.new(),
    )

    assert decision.approved
    assert swap.status == ExchangeStatus.APPROVED
    assert isinstance(swap.pull_domain_events()[0], OfficialSwapApproved)


def test_official_swap_denied_by_rest() -> None:
    first = _military(1)
    second = _military(2)
    service_scale, role = _scale()
    first_assignment = _assignment(service_scale, role, first, 2026, 7, 10)
    second_assignment = _assignment(service_scale, role, second, 2026, 7, 11)
    previous = _assignment(service_scale, role, second, 2026, 7, 9)
    swap = OfficialSwap.request(first.id, ExchangeReason("Troca por necessidade do servico"), first_assignment, second_assignment)

    decision = SwapValidationEngine().evaluate(
        swap=swap,
        source_military=first,
        target_military=second,
        service_scale=service_scale,
        source_role=role,
        target_role=role,
        history=(previous,),
        decided_by=Identity.new(),
    )

    assert not decision.approved
    assert EligibilityReason.INSUFFICIENT_REST in decision.reasons
    assert swap.status == ExchangeStatus.REJECTED
    assert isinstance(swap.pull_domain_events()[0], OfficialSwapRejected)


def test_official_swap_with_formal_exception() -> None:
    first = _military(1)
    second = _military(2)
    service_scale, role = _scale()
    first_assignment = _assignment(service_scale, role, first, 2026, 7, 10)
    second_assignment = _assignment(service_scale, role, second, 2026, 7, 11)
    previous = _assignment(service_scale, role, second, 2026, 7, 8)
    swap = OfficialSwap.request(first.id, ExchangeReason("Excecao formal autorizada"), first_assignment, second_assignment)

    decision = SwapValidationEngine(OfficialSwapPolicy(allow_formal_rest_exception=True)).evaluate(
        swap=swap,
        source_military=first,
        target_military=second,
        service_scale=service_scale,
        source_role=role,
        target_role=role,
        history=(previous,),
        decided_by=Identity.new(),
    )

    assert decision.approved
    assert decision.metadata["formal_rest_exception"] is True


def test_valid_service_sale() -> None:
    seller = _military(1)
    buyer = _military(2)
    service_scale, role = _scale()
    seller_assignment = _assignment(service_scale, role, seller, 2026, 7, 20)
    buyer_assignment = _assignment(service_scale, role, buyer, 2026, 7, 25)
    sale = ServiceSale.request(seller.id, ExchangeReason("Venda autorizada pelo comando"), seller_assignment, buyer_assignment)

    decision = ServiceSaleEngine().evaluate(
        sale=sale,
        buyer=buyer,
        service_scale=service_scale,
        seller_role=role,
        history=(),
        decided_by=Identity.new(),
    )

    assert decision.approved
    assert sale.status == ExchangeStatus.APPROVED
    assert sale.buyer_assumes_extraordinary_service
    assert sale.buyer_counter_preserved
    assert sale.seller_counter_resets_normally
    assert isinstance(sale.pull_domain_events()[0], ServiceSaleApproved)


def test_service_sale_denied_by_buyer_ineligibility() -> None:
    seller = _military(1)
    buyer = _military(2)
    buyer.deactivate("Restricao operacional")
    service_scale, role = _scale()
    seller_assignment = _assignment(service_scale, role, seller, 2026, 7, 20)
    buyer_assignment = _assignment(service_scale, role, buyer, 2026, 7, 25)
    sale = ServiceSale.request(seller.id, ExchangeReason("Venda solicitada ao comando"), seller_assignment, buyer_assignment)

    decision = ServiceSaleEngine().evaluate(
        sale=sale,
        buyer=buyer,
        service_scale=service_scale,
        seller_role=role,
        history=(),
        decided_by=Identity.new(),
    )

    assert not decision.approved
    assert EligibilityReason.MILITARY_INACTIVE in decision.reasons
    assert sale.status == ExchangeStatus.REJECTED
    assert isinstance(sale.pull_domain_events()[0], ServiceSaleRejected)


def test_service_sale_preserves_buyer_counter_and_resets_seller_counter() -> None:
    seller = _military(1)
    buyer = _military(2)
    service_scale, role = _scale()
    seller_assignment = _assignment(service_scale, role, seller, 2026, 7, 20)
    buyer_assignment = _assignment(service_scale, role, buyer, 2026, 7, 25)
    sale = ServiceSale.request(seller.id, ExchangeReason("Venda com registro extraordinario"), seller_assignment, buyer_assignment)

    ServiceSaleEngine(ServiceSalePolicy()).evaluate(
        sale=sale,
        buyer=buyer,
        service_scale=service_scale,
        seller_role=role,
        history=(),
        decided_by=Identity.new(),
    )

    assert sale.buyer_counter_preserved is True
    assert sale.seller_counter_resets_normally is True
    assert sale.buyer_assignment == buyer_assignment
    assert sale.seller_assignment == seller_assignment

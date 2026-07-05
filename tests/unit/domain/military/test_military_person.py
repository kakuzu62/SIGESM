from __future__ import annotations

import pytest

from domain.military.entities import MilitaryPerson
from domain.military.events import MilitaryRegistered
from domain.military.exceptions import (
    InvalidCPFException,
    InvalidFullNameException,
    MilitaryDomainException,
)
from domain.military.value_objects import CPF, FullName, MilitaryId, MilitaryStatus, Phone, Rank


def _register_person() -> MilitaryPerson:
    return MilitaryPerson.register(
        military_id=MilitaryId(" eb-001 "),
        full_name=FullName("Joao da Silva"),
        cpf=CPF("529.982.247-25"),
        rank=Rank("Cabo"),
        phone=Phone("(11) 98888-7777"),
    )


def test_register_military_person_sets_initial_state() -> None:
    person = _register_person()

    assert person.military_id.value == "EB-001"
    assert person.full_name.value == "Joao da Silva"
    assert person.cpf.value == "52998224725"
    assert person.rank == Rank("CB")
    assert person.phone.value == "+5511988887777"
    assert person.status == MilitaryStatus.ACTIVE
    assert person.created_at == person.updated_at


def test_valid_and_invalid_cpf() -> None:
    cpf = CPF("52998224725")

    assert cpf.formatted == "529.982.247-25"

    with pytest.raises(InvalidCPFException):
        CPF("111.111.111-11")


def test_invalid_full_name() -> None:
    with pytest.raises(InvalidFullNameException):
        FullName("Joao")


def test_change_rank_uses_hierarchical_rank_value_object() -> None:
    person = _register_person()

    person.change_rank(Rank("3 Sgt"))

    assert person.rank > Rank("Cabo")
    assert person.rank.value == "3 SARGENTO"


def test_activate_and_deactivate() -> None:
    person = _register_person()

    person.deactivate("Transferred to reserve")
    assert person.status == MilitaryStatus.INACTIVE

    another_person = _register_person()
    another_person.deactivate("Administrative update")
    another_person.activate()
    assert another_person.status == MilitaryStatus.ACTIVE

    with pytest.raises(MilitaryDomainException):
        person.deactivate(" ")


def test_update_contact_normalizes_brazilian_phone() -> None:
    person = _register_person()

    person.update_contact(Phone("2133334444"))

    assert person.phone.value == "+552133334444"


def test_register_emits_military_registered_event() -> None:
    person = _register_person()

    events = person.pull_domain_events()

    assert len(events) == 1
    assert isinstance(events[0], MilitaryRegistered)
    assert events[0].military_person_id == person.id
    assert events[0].military_id == "EB-001"

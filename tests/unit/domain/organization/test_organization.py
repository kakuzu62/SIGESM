from __future__ import annotations

from collections.abc import Sequence

import pytest

from domain.organization.entities import Organization
from domain.organization.events import OrganizationCreated
from domain.organization.exceptions import (
    InvalidAbbreviationException,
    InvalidLocationException,
    InvalidOrganizationCodeException,
    InvalidOrganizationNameException,
)
from domain.organization.repositories import IOrganizationRepository
from domain.organization.specifications import OrganizationCodeAlreadyExists
from domain.organization.value_objects import (
    Abbreviation,
    City,
    Country,
    OrganizationCode,
    OrganizationName,
    State,
)
from shared.kernel.identity import Identity


class InMemoryOrganizationRepository(IOrganizationRepository):
    """In-memory repository used only by organization unit tests."""

    def __init__(self, organizations: Sequence[Organization] = ()) -> None:
        self._organizations = list(organizations)

    def add(self, entity: Organization) -> Organization:
        """Add an organization."""
        self._organizations.append(entity)
        return entity

    def update(self, entity: Organization) -> Organization:
        """Update an organization."""
        self.delete(entity)
        self._organizations.append(entity)
        return entity

    def delete(self, entity: Organization) -> None:
        """Delete an organization."""
        self._organizations = [item for item in self._organizations if item.id != entity.id]

    def get_by_id(self, entity_id: Identity) -> Organization | None:
        """Return an organization by identity."""
        return next((item for item in self._organizations if item.id == entity_id), None)

    def exists(self, entity_id: Identity) -> bool:
        """Return whether an organization identity exists."""
        return self.get_by_id(entity_id) is not None

    def count(self) -> int:
        """Return organization count."""
        return len(self._organizations)

    def list(self) -> Sequence[Organization]:
        """Return all organizations."""
        return tuple(self._organizations)

    def first(self) -> Organization | None:
        """Return the first organization."""
        return self._organizations[0] if self._organizations else None

    def get_by_code(self, code: OrganizationCode) -> Organization | None:
        """Return an organization by code."""
        return next((item for item in self._organizations if item.code == code), None)

    def code_exists(self, code: OrganizationCode) -> bool:
        """Return whether an organization code exists."""
        return self.get_by_code(code) is not None


def _create_organization() -> Organization:
    return Organization.create(
        code=OrganizationCode(" 1-bda-inf "),
        name=OrganizationName("Primeira Brigada de Infantaria"),
        abbreviation=Abbreviation("1 BDA INF"),
        city=City("Rio de Janeiro"),
        state=State("RJ"),
        country=Country.brazil(),
    )


def test_create_organization_sets_initial_state_and_event() -> None:
    organization = _create_organization()

    assert organization.code.value == "1-BDA-INF"
    assert organization.name.value == "Primeira Brigada de Infantaria"
    assert organization.abbreviation.value == "1BDAINF"
    assert organization.city.value == "Rio de Janeiro"
    assert organization.state.value == "RJ"
    assert organization.country.value == "Brasil"
    assert organization.created_at == organization.updated_at

    events = organization.pull_domain_events()
    assert len(events) == 1
    assert isinstance(events[0], OrganizationCreated)
    assert events[0].organization_id == organization.id
    assert events[0].code == "1-BDA-INF"


def test_organization_can_be_renamed_and_relocated() -> None:
    organization = _create_organization()

    organization.rename(
        name=OrganizationName("Primeira Brigada de Infantaria de Selva"),
        abbreviation=Abbreviation("1 Bda Inf Sl"),
    )
    organization.relocate(city=City("Manaus"), state=State("AM"), country=Country("Brasil"))

    assert organization.name.value == "Primeira Brigada de Infantaria de Selva"
    assert organization.abbreviation.value == "1BDAINFSL"
    assert organization.city.value == "Manaus"
    assert organization.state.value == "AM"


def test_value_objects_validate_invalid_values() -> None:
    with pytest.raises(InvalidOrganizationCodeException):
        OrganizationCode("@")

    with pytest.raises(InvalidOrganizationNameException):
        OrganizationName("OM")

    with pytest.raises(InvalidAbbreviationException):
        Abbreviation(" ")

    with pytest.raises(InvalidLocationException):
        City("A")

    with pytest.raises(InvalidLocationException):
        State("XX")

    with pytest.raises(InvalidLocationException):
        Country("B")


def test_organization_code_already_exists_specification() -> None:
    organization = _create_organization()
    repository = InMemoryOrganizationRepository((organization,))
    specification = OrganizationCodeAlreadyExists(repository)

    assert specification.is_satisfied_by(OrganizationCode("1-BDA-INF"))
    assert not specification.is_satisfied_by(OrganizationCode("2-BDA-INF"))

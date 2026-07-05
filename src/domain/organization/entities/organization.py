from __future__ import annotations

from datetime import UTC, datetime

from domain.organization.events import OrganizationCreated
from domain.organization.value_objects import (
    Abbreviation,
    City,
    Country,
    OrganizationCode,
    OrganizationName,
    State,
)
from shared.kernel.aggregate_root import AggregateRoot
from shared.kernel.identity import Identity


class Organization(AggregateRoot[Identity]):
    """Aggregate root representing a military organization."""

    __slots__ = (
        "_code",
        "_name",
        "_abbreviation",
        "_city",
        "_state",
        "_country",
        "_created_at",
        "_updated_at",
    )

    def __init__(
        self,
        entity_id: Identity,
        code: OrganizationCode,
        name: OrganizationName,
        abbreviation: Abbreviation,
        city: City,
        state: State,
        country: Country,
        created_at: datetime,
        updated_at: datetime,
    ) -> None:
        super().__init__(entity_id)
        self._code = code
        self._name = name
        self._abbreviation = abbreviation
        self._city = city
        self._state = state
        self._country = country
        self._created_at = created_at
        self._updated_at = updated_at

    @classmethod
    def create(
        cls,
        code: OrganizationCode,
        name: OrganizationName,
        abbreviation: Abbreviation,
        city: City,
        state: State,
        country: Country,
    ) -> Organization:
        """Create an organization and record the creation domain event."""
        now = datetime.now(UTC)
        organization = cls(
            entity_id=Identity.new(),
            code=code,
            name=name,
            abbreviation=abbreviation,
            city=city,
            state=state,
            country=country,
            created_at=now,
            updated_at=now,
        )
        organization.add_domain_event(
            OrganizationCreated(organization_id=organization.id, code=organization.code.value)
        )
        return organization

    @property
    def code(self) -> OrganizationCode:
        """Return organization code."""
        return self._code

    @property
    def name(self) -> OrganizationName:
        """Return organization name."""
        return self._name

    @property
    def abbreviation(self) -> Abbreviation:
        """Return organization abbreviation."""
        return self._abbreviation

    @property
    def city(self) -> City:
        """Return organization city."""
        return self._city

    @property
    def state(self) -> State:
        """Return organization state."""
        return self._state

    @property
    def country(self) -> Country:
        """Return organization country."""
        return self._country

    @property
    def created_at(self) -> datetime:
        """Return creation timestamp."""
        return self._created_at

    @property
    def updated_at(self) -> datetime:
        """Return last update timestamp."""
        return self._updated_at

    def rename(self, name: OrganizationName, abbreviation: Abbreviation) -> None:
        """Update organization official name and abbreviation."""
        self._name = name
        self._abbreviation = abbreviation
        self._touch()

    def relocate(self, city: City, state: State, country: Country) -> None:
        """Update organization location."""
        self._city = city
        self._state = state
        self._country = country
        self._touch()

    def _touch(self) -> None:
        """Update modification timestamp."""
        self._updated_at = datetime.now(UTC)

from __future__ import annotations

from datetime import UTC, datetime

from domain.military.events import MilitaryRegistered
from domain.military.exceptions import MilitaryDomainException
from domain.military.value_objects import CPF, FullName, MilitaryId, MilitaryStatus, Phone, Rank
from shared.kernel.aggregate_root import AggregateRoot
from shared.kernel.identity import Identity


class MilitaryPerson(AggregateRoot[Identity]):
    """Aggregate root representing a registered military person."""

    __slots__ = (
        "_military_id",
        "_full_name",
        "_cpf",
        "_rank",
        "_phone",
        "_status",
        "_created_at",
        "_updated_at",
    )

    def __init__(
        self,
        entity_id: Identity,
        military_id: MilitaryId,
        full_name: FullName,
        cpf: CPF,
        rank: Rank,
        phone: Phone,
        status: MilitaryStatus,
        created_at: datetime,
        updated_at: datetime,
    ) -> None:
        super().__init__(entity_id)
        self._military_id = military_id
        self._full_name = full_name
        self._cpf = cpf
        self._rank = rank
        self._phone = phone
        self._status = status
        self._created_at = created_at
        self._updated_at = updated_at

    @classmethod
    def register(
        cls,
        military_id: MilitaryId,
        full_name: FullName,
        cpf: CPF,
        rank: Rank,
        phone: Phone,
    ) -> MilitaryPerson:
        """Create a military person and record the registration domain event."""
        now = datetime.now(UTC)
        person = cls(
            entity_id=Identity.new(),
            military_id=military_id,
            full_name=full_name,
            cpf=cpf,
            rank=rank,
            phone=phone,
            status=MilitaryStatus.ACTIVE,
            created_at=now,
            updated_at=now,
        )
        person.add_domain_event(
            MilitaryRegistered(military_person_id=person.id, military_id=person.military_id.value)
        )
        return person

    @property
    def military_id(self) -> MilitaryId:
        """Return military identifier."""
        return self._military_id

    @property
    def full_name(self) -> FullName:
        """Return full name."""
        return self._full_name

    @property
    def cpf(self) -> CPF:
        """Return CPF."""
        return self._cpf

    @property
    def rank(self) -> Rank:
        """Return current rank."""
        return self._rank

    @property
    def phone(self) -> Phone:
        """Return contact phone."""
        return self._phone

    @property
    def status(self) -> MilitaryStatus:
        """Return current military status."""
        return self._status

    @property
    def created_at(self) -> datetime:
        """Return registration timestamp."""
        return self._created_at

    @property
    def updated_at(self) -> datetime:
        """Return last update timestamp."""
        return self._updated_at

    def activate(self) -> None:
        """Activate the military person."""
        if self._status == MilitaryStatus.ACTIVE:
            return

        self._status = MilitaryStatus.ACTIVE
        self._touch()

    def deactivate(self, reason: str) -> None:
        """Deactivate the military person with a required reason."""
        if not reason.strip():
            raise MilitaryDomainException("Deactivation reason is required.")

        self._status = MilitaryStatus.INACTIVE
        self._touch()

    def update_contact(self, phone: Phone) -> None:
        """Update contact phone."""
        self._phone = phone
        self._touch()

    def change_rank(self, rank: Rank) -> None:
        """Change rank or graduation."""
        self._rank = rank
        self._touch()

    def _touch(self) -> None:
        """Update the aggregate modification timestamp."""
        self._updated_at = datetime.now(UTC)

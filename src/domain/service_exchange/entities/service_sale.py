from __future__ import annotations

from datetime import UTC, datetime

from domain.service_exchange.events import ServiceSaleApproved, ServiceSaleRejected
from domain.service_exchange.exceptions import InvalidExchangeOperationException
from domain.service_exchange.value_objects import ExchangeReason, ExchangeStatus
from domain.service_scale.entities import ServiceAssignment
from shared.kernel.aggregate_root import AggregateRoot
from shared.kernel.identity import Identity


class ServiceSale(AggregateRoot[Identity]):
    """Aggregate root representing an extraordinary service sale/transfer."""

    __slots__ = (
        "_requested_by",
        "_approved_by",
        "_status",
        "_reason",
        "_seller_assignment",
        "_buyer_assignment",
        "_buyer_assumes_extraordinary_service",
        "_seller_counter_resets_normally",
        "_buyer_counter_preserved",
        "_created_at",
        "_updated_at",
        "_approved_at",
        "_rejected_at",
    )

    def __init__(
        self,
        entity_id: Identity,
        requested_by: Identity,
        reason: ExchangeReason,
        seller_assignment: ServiceAssignment,
        buyer_assignment: ServiceAssignment,
        created_at: datetime,
        updated_at: datetime,
        status: ExchangeStatus = ExchangeStatus.REQUESTED,
        approved_by: Identity | None = None,
        approved_at: datetime | None = None,
        rejected_at: datetime | None = None,
        buyer_assumes_extraordinary_service: bool = False,
        seller_counter_resets_normally: bool = False,
        buyer_counter_preserved: bool = True,
    ) -> None:
        super().__init__(entity_id)
        self._requested_by = requested_by
        self._approved_by = approved_by
        self._status = status
        self._reason = reason
        self._seller_assignment = seller_assignment
        self._buyer_assignment = buyer_assignment
        self._created_at = created_at
        self._updated_at = updated_at
        self._approved_at = approved_at
        self._rejected_at = rejected_at
        self._buyer_assumes_extraordinary_service = buyer_assumes_extraordinary_service
        self._seller_counter_resets_normally = seller_counter_resets_normally
        self._buyer_counter_preserved = buyer_counter_preserved

    @classmethod
    def request(
        cls,
        requested_by: Identity,
        reason: ExchangeReason,
        seller_assignment: ServiceAssignment,
        buyer_assignment: ServiceAssignment,
    ) -> ServiceSale:
        """Request a service sale."""
        now = datetime.now(UTC)
        return cls(
            entity_id=Identity.new(),
            requested_by=requested_by,
            reason=reason,
            seller_assignment=seller_assignment,
            buyer_assignment=buyer_assignment,
            created_at=now,
            updated_at=now,
        )

    @property
    def requested_by(self) -> Identity:
        """Return requester identity."""
        return self._requested_by

    @property
    def approved_by(self) -> Identity | None:
        """Return approver identity when approved."""
        return self._approved_by

    @property
    def status(self) -> ExchangeStatus:
        """Return current sale status."""
        return self._status

    @property
    def reason(self) -> ExchangeReason:
        """Return sale reason."""
        return self._reason

    @property
    def seller_assignment(self) -> ServiceAssignment:
        """Return assignment sold by the seller."""
        return self._seller_assignment

    @property
    def buyer_assignment(self) -> ServiceAssignment:
        """Return buyer base assignment that must preserve its counter."""
        return self._buyer_assignment

    @property
    def buyer_assumes_extraordinary_service(self) -> bool:
        """Return whether buyer assumes extraordinary service."""
        return self._buyer_assumes_extraordinary_service

    @property
    def seller_counter_resets_normally(self) -> bool:
        """Return whether seller counter resets as if service was completed."""
        return self._seller_counter_resets_normally

    @property
    def buyer_counter_preserved(self) -> bool:
        """Return whether buyer base counter remains preserved."""
        return self._buyer_counter_preserved

    @property
    def created_at(self) -> datetime:
        """Return creation timestamp."""
        return self._created_at

    @property
    def updated_at(self) -> datetime:
        """Return update timestamp."""
        return self._updated_at

    @property
    def approved_at(self) -> datetime | None:
        """Return approval timestamp."""
        return self._approved_at

    @property
    def rejected_at(self) -> datetime | None:
        """Return rejection timestamp."""
        return self._rejected_at

    def approve(self, approved_by: Identity) -> None:
        """Approve service sale and mark operational counter semantics."""
        self._ensure_requested()
        now = datetime.now(UTC)
        self._approved_by = approved_by
        self._approved_at = now
        self._updated_at = now
        self._status = ExchangeStatus.APPROVED
        self._buyer_assumes_extraordinary_service = True
        self._seller_counter_resets_normally = True
        self._buyer_counter_preserved = True
        self.add_domain_event(ServiceSaleApproved(sale_id=self.id, approved_by=approved_by))

    def reject(self, reasons: tuple[str, ...]) -> None:
        """Reject service sale and emit an auditable event."""
        self._ensure_requested()
        now = datetime.now(UTC)
        self._rejected_at = now
        self._updated_at = now
        self._status = ExchangeStatus.REJECTED
        self.add_domain_event(ServiceSaleRejected(sale_id=self.id, reasons=reasons))

    def _ensure_requested(self) -> None:
        if self._status != ExchangeStatus.REQUESTED:
            raise InvalidExchangeOperationException("Only requested service sales can be decided.")

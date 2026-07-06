from __future__ import annotations

from datetime import UTC, datetime

from domain.service_exchange.events import OfficialSwapApproved, OfficialSwapRejected
from domain.service_exchange.exceptions import InvalidExchangeOperationException
from domain.service_exchange.value_objects import ExchangeReason, ExchangeStatus
from domain.service_scale.entities import ServiceAssignment
from shared.kernel.aggregate_root import AggregateRoot
from shared.kernel.identity import Identity


class OfficialSwap(AggregateRoot[Identity]):
    """Aggregate root representing a real service day swap between two military persons."""

    __slots__ = (
        "_requested_by",
        "_approved_by",
        "_status",
        "_reason",
        "_source_assignment",
        "_target_assignment",
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
        source_assignment: ServiceAssignment,
        target_assignment: ServiceAssignment,
        created_at: datetime,
        updated_at: datetime,
        status: ExchangeStatus = ExchangeStatus.REQUESTED,
        approved_by: Identity | None = None,
        approved_at: datetime | None = None,
        rejected_at: datetime | None = None,
    ) -> None:
        super().__init__(entity_id)
        self._requested_by = requested_by
        self._approved_by = approved_by
        self._status = status
        self._reason = reason
        self._source_assignment = source_assignment
        self._target_assignment = target_assignment
        self._created_at = created_at
        self._updated_at = updated_at
        self._approved_at = approved_at
        self._rejected_at = rejected_at

    @classmethod
    def request(
        cls,
        requested_by: Identity,
        reason: ExchangeReason,
        source_assignment: ServiceAssignment,
        target_assignment: ServiceAssignment,
    ) -> OfficialSwap:
        """Request an official service swap."""
        now = datetime.now(UTC)
        return cls(
            entity_id=Identity.new(),
            requested_by=requested_by,
            reason=reason,
            source_assignment=source_assignment,
            target_assignment=target_assignment,
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
        """Return current exchange status."""
        return self._status

    @property
    def reason(self) -> ExchangeReason:
        """Return exchange reason."""
        return self._reason

    @property
    def source_assignment(self) -> ServiceAssignment:
        """Return assignment originally held by the requester side."""
        return self._source_assignment

    @property
    def target_assignment(self) -> ServiceAssignment:
        """Return assignment originally held by the counterpart side."""
        return self._target_assignment

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
        """Approve the official swap and emit an auditable event."""
        self._ensure_requested()
        now = datetime.now(UTC)
        self._approved_by = approved_by
        self._approved_at = now
        self._updated_at = now
        self._status = ExchangeStatus.APPROVED
        self.add_domain_event(OfficialSwapApproved(swap_id=self.id, approved_by=approved_by))

    def reject(self, reasons: tuple[str, ...]) -> None:
        """Reject the official swap and emit an auditable event."""
        self._ensure_requested()
        now = datetime.now(UTC)
        self._rejected_at = now
        self._updated_at = now
        self._status = ExchangeStatus.REJECTED
        self.add_domain_event(OfficialSwapRejected(swap_id=self.id, reasons=reasons))

    def _ensure_requested(self) -> None:
        if self._status != ExchangeStatus.REQUESTED:
            raise InvalidExchangeOperationException("Only requested official swaps can be decided.")

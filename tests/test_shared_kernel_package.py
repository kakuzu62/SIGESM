from __future__ import annotations

import pytest

from bootstrap.container import Container
from core.exceptions.configuration import ConfigurationException
from core.exceptions.validation import ValidationException
from shared.kernel import (
    AggregateRoot,
    DomainEvent,
    Entity,
    EventDispatcher,
    Guard,
    Identity,
    Notification,
    Result,
    Specification,
    ValueObject,
)


class Customer(Entity[Identity]):
    """Entity used by shared kernel tests."""


class CustomerAggregate(AggregateRoot[Identity]):
    """Aggregate root used by shared kernel tests."""


class Money(ValueObject):
    """Value object used by shared kernel tests."""

    __slots__ = ("amount", "currency")
    amount: int
    currency: str

    def __init__(self, amount: int, currency: str) -> None:
        object.__setattr__(self, "amount", amount)
        object.__setattr__(self, "currency", currency)
        super().__init__()

    @property
    def equality_components(self) -> tuple[int, str]:
        """Return values that define equality."""
        return (self.amount, self.currency)


class CustomerCreated(DomainEvent):
    """Domain event used by shared kernel tests."""


class GreaterThan(Specification[int]):
    """Specification that validates a lower bound."""

    def __init__(self, minimum: int) -> None:
        self._minimum = minimum

    def is_satisfied_by(self, candidate: int) -> bool:
        """Return whether candidate is greater than the configured minimum."""
        return candidate > self._minimum


class LessThan(Specification[int]):
    """Specification that validates an upper bound."""

    def __init__(self, maximum: int) -> None:
        self._maximum = maximum

    def is_satisfied_by(self, candidate: int) -> bool:
        """Return whether candidate is lower than the configured maximum."""
        return candidate < self._maximum


def test_entity_identity_is_immutable_and_compared_by_identity() -> None:
    identity = Identity.new()
    customer = Customer(identity)
    same_customer = Customer(identity)

    assert customer == same_customer
    assert hash(customer) == hash(same_customer)

    with pytest.raises(AttributeError):
        setattr(customer, "id", Identity.new())


def test_aggregate_root_tracks_and_pulls_domain_events() -> None:
    aggregate = CustomerAggregate(Identity.new())
    event = CustomerCreated()

    aggregate.add_domain_event(event)

    assert aggregate.pull_domain_events() == (event,)
    assert aggregate.pull_domain_events() == ()


def test_value_object_and_identity_are_immutable_and_value_based() -> None:
    first = Money(10, "BRL")
    second = Money(10, "BRL")
    identity = Identity.from_string(str(Identity.new()))

    assert first == second
    assert str(identity) == str(identity.value)

    with pytest.raises(AttributeError):
        first.amount = 20


def test_result_controls_success_and_failure_access() -> None:
    success = Result.success("ok")
    failure = Result[str].failure("invalid")

    assert success.is_success
    assert failure.is_failure
    assert success.value == "ok"
    assert failure.error == "invalid"

    with pytest.raises(ValidationException):
        _ = success.error

    with pytest.raises(ValidationException):
        _ = failure.value


def test_notification_collects_errors_by_field() -> None:
    notification = Notification()

    notification.add_error("name", "required")
    notification.add_error("name", "too short")

    assert notification.has_errors
    assert len(notification.errors) == 2
    assert len(notification.errors_for("name")) == 2


def test_guard_clauses_raise_validation_exceptions() -> None:
    assert Guard.against_none("SIGESM", "name") == "SIGESM"
    assert Guard.against_empty("Enterprise", "name") == "Enterprise"
    assert Guard.against_negative(0, "quantity") == 0
    assert Guard.against_zero_or_negative(1, "quantity") == 1
    assert Guard.against_max_length("abc", 3, "code") == "abc"
    assert Guard.against_min_length("abc", 3, "code") == "abc"

    with pytest.raises(ValidationException):
        Guard.against_empty(" ", "name")


def test_event_dispatcher_invokes_registered_handlers() -> None:
    dispatcher = EventDispatcher()
    handled_events: list[str] = []

    dispatcher.register(CustomerCreated, lambda event: handled_events.append(event.event_name))
    dispatcher.dispatch(CustomerCreated())

    assert handled_events == ["CustomerCreated"]


def test_specification_composition() -> None:
    between_one_and_ten = GreaterThan(1) & LessThan(10)
    outside_range = ~between_one_and_ten

    assert between_one_and_ten.is_satisfied_by(5)
    assert not between_one_and_ten.is_satisfied_by(10)
    assert (GreaterThan(10) | LessThan(3)).is_satisfied_by(2)
    assert outside_range.is_satisfied_by(10)


def test_container_resolves_singletons_and_factories() -> None:
    container = Container()

    container.register_singleton(str, "SIGESM")
    container.register_factory(int, lambda: 42)

    assert container.contains(str)
    assert container.resolve(str) == "SIGESM"
    assert container.resolve(int) == 42

    container.clear()

    with pytest.raises(ConfigurationException):
        container.resolve(str)

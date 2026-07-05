from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Generic, TypeVar

T = TypeVar("T")


class Specification(ABC, Generic[T]):
    """Base specification used to compose domain predicates."""

    @abstractmethod
    def is_satisfied_by(self, candidate: T) -> bool:
        """Return whether the candidate satisfies this specification."""
        raise NotImplementedError

    def __and__(self, other: Specification[T]) -> Specification[T]:
        return _AndSpecification(self, other)

    def __or__(self, other: Specification[T]) -> Specification[T]:
        return _OrSpecification(self, other)

    def __invert__(self) -> Specification[T]:
        return _NotSpecification(self)


class _AndSpecification(Specification[T]):
    """Specification that requires both operands to be satisfied."""

    def __init__(self, left: Specification[T], right: Specification[T]) -> None:
        self._left = left
        self._right = right

    def is_satisfied_by(self, candidate: T) -> bool:
        """Return whether both specifications are satisfied."""
        return self._left.is_satisfied_by(candidate) and self._right.is_satisfied_by(candidate)


class _OrSpecification(Specification[T]):
    """Specification that requires at least one operand to be satisfied."""

    def __init__(self, left: Specification[T], right: Specification[T]) -> None:
        self._left = left
        self._right = right

    def is_satisfied_by(self, candidate: T) -> bool:
        """Return whether any specification is satisfied."""
        return self._left.is_satisfied_by(candidate) or self._right.is_satisfied_by(candidate)


class _NotSpecification(Specification[T]):
    """Specification that negates another specification."""

    def __init__(self, wrapped: Specification[T]) -> None:
        self._wrapped = wrapped

    def is_satisfied_by(self, candidate: T) -> bool:
        """Return the negated result of the wrapped specification."""
        return not self._wrapped.is_satisfied_by(candidate)

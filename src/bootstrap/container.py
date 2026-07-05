from __future__ import annotations

from collections.abc import Callable
from typing import Any, TypeVar, cast

from core.exceptions.configuration import ConfigurationException

T = TypeVar("T")


class Container:
    """Minimal dependency injection container for application composition."""

    def __init__(self) -> None:
        self._singletons: dict[type[Any], Any] = {}
        self._factories: dict[type[Any], Callable[[], Any]] = {}

    def register_singleton(self, dependency_type: type[T], instance: T) -> None:
        """Register a singleton instance for a dependency type."""
        self._singletons[dependency_type] = instance
        self._factories.pop(dependency_type, None)

    def register_factory(self, dependency_type: type[T], factory: Callable[[], T]) -> None:
        """Register a factory function for a dependency type."""
        self._factories[dependency_type] = factory
        self._singletons.pop(dependency_type, None)

    def resolve(self, dependency_type: type[T]) -> T:
        """Resolve a dependency or raise a clear configuration error."""
        if dependency_type in self._singletons:
            return cast(T, self._singletons[dependency_type])

        if dependency_type in self._factories:
            return cast(T, self._factories[dependency_type]())

        raise ConfigurationException(f"Dependency not registered: {dependency_type.__qualname__}")

    def contains(self, dependency_type: type[Any]) -> bool:
        """Return whether a dependency type has a registered provider."""
        return dependency_type in self._singletons or dependency_type in self._factories

    def clear(self) -> None:
        """Remove all registered dependencies."""
        self._singletons.clear()
        self._factories.clear()

from __future__ import annotations

from collections.abc import Callable


class Command:
    """Executable command used by view models."""

    def __init__(
        self,
        execute: Callable[[], None],
        can_execute: Callable[[], bool] | None = None,
    ) -> None:
        self._execute = execute
        self._can_execute = can_execute or (lambda: True)
        self._changed_handlers: list[Callable[[], None]] = []

    def execute(self) -> None:
        """Execute the command when it is enabled."""
        if self.can_execute():
            self._execute()

    def can_execute(self) -> bool:
        """Return whether the command can be executed."""
        return self._can_execute()

    def subscribe_changed(self, handler: Callable[[], None]) -> None:
        """Subscribe to command state changes."""
        self._changed_handlers.append(handler)

    def notify_changed(self) -> None:
        """Notify listeners that command state changed."""
        for handler in tuple(self._changed_handlers):
            handler()

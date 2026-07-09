from __future__ import annotations


class NavigationHistory:
    """Tracks navigation back and forward stacks."""

    def __init__(self) -> None:
        self._back_stack: list[str] = []
        self._forward_stack: list[str] = []
        self._current: str | None = None

    @property
    def current(self) -> str | None:
        """Return the current navigation key."""
        return self._current

    def record(self, key: str) -> None:
        """Record a new navigation target."""
        if self._current is not None and self._current != key:
            self._back_stack.append(self._current)
        if self._current != key:
            self._forward_stack.clear()
        self._current = key

    def back(self) -> str | None:
        """Move backward in history."""
        if not self._back_stack:
            return None
        if self._current is not None:
            self._forward_stack.append(self._current)
        self._current = self._back_stack.pop()
        return self._current

    def forward(self) -> str | None:
        """Move forward in history."""
        if not self._forward_stack:
            return None
        if self._current is not None:
            self._back_stack.append(self._current)
        self._current = self._forward_stack.pop()
        return self._current

    def clear(self) -> None:
        """Clear all navigation history."""
        self._back_stack.clear()
        self._forward_stack.clear()
        self._current = None

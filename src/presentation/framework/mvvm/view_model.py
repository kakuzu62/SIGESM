from __future__ import annotations

from presentation.framework.mvvm.observable_object import ObservableObject


class ViewModel(ObservableObject):
    """Base class for desktop view models."""

    def on_loaded(self) -> None:
        """Run when the associated view is loaded."""

    def on_unloaded(self) -> None:
        """Run when the associated view is unloaded."""

    def dispose(self) -> None:
        """Release resources owned by the view model."""

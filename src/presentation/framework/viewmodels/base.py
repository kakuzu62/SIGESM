from __future__ import annotations

from presentation.framework.mvvm import ViewModel


class ObservableViewModel(ViewModel):
    """Base view model with change notification hooks."""

    def notify_changed(self, property_name: str) -> None:
        """Notify listeners that a property changed."""
        self.notify_property_changed(property_name)

from __future__ import annotations

from presentation.framework.mvvm import ViewModel


class ScaleViewModel(ViewModel):
    """View model for the scale module placeholder."""

    @property
    def status_message(self) -> str:
        """Return the module status message."""
        return "Modulo em desenvolvimento."

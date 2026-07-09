from __future__ import annotations

from presentation.framework.mvvm import ViewModel


class SettingsViewModel(ViewModel):
    """View model for the settings module placeholder."""

    @property
    def status_message(self) -> str:
        """Return the module status message."""
        return "Modulo em desenvolvimento."

from __future__ import annotations

from PySide6.QtWidgets import QMessageBox, QWidget


class ConfirmationDialog:
    """Reusable confirmation dialog."""

    def confirm(self, parent: QWidget | None, title: str, message: str) -> bool:
        """Ask the user to confirm an action."""
        result = QMessageBox.question(parent, title, message)
        return result == QMessageBox.StandardButton.Yes

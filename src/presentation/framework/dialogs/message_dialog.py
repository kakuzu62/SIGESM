from __future__ import annotations

from PySide6.QtWidgets import QMessageBox, QWidget

from presentation.framework.dialogs.dialog_service import DialogRequest, DialogResult


class MessageDialog:
    """Displays standard message dialogs."""

    def show(self, parent: QWidget | None, request: DialogRequest) -> DialogResult:
        """Show a message dialog and return the user decision."""
        box = QMessageBox(parent)
        box.setWindowTitle(request.title)
        box.setText(request.message)
        box.setIcon(self._icon_for(request.severity))
        box.setStandardButtons(QMessageBox.StandardButton.Ok)
        result = box.exec()
        return DialogResult(accepted=result == QMessageBox.StandardButton.Ok)

    @staticmethod
    def _icon_for(severity: str) -> QMessageBox.Icon:
        if severity == "warning":
            return QMessageBox.Icon.Warning
        if severity == "error":
            return QMessageBox.Icon.Critical
        return QMessageBox.Icon.Information

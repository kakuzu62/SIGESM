from __future__ import annotations

from PySide6.QtWidgets import QDialog, QFormLayout, QHBoxLayout, QLineEdit, QPushButton, QVBoxLayout


class ResetPasswordDialog(QDialog):
    """Dialog for password reset."""

    def __init__(self) -> None:
        super().__init__()
        self._password = QLineEdit()
        self._password.setEchoMode(QLineEdit.EchoMode.Password)
        self._build()

    @property
    def password(self) -> str:
        """Return typed password."""
        return self._password.text()

    def _build(self) -> None:
        self.setWindowTitle("Redefinir senha")
        form = QFormLayout()
        form.addRow("Nova senha", self._password)
        save = QPushButton("Salvar")
        cancel = QPushButton("Cancelar")
        save.clicked.connect(self.accept)
        cancel.clicked.connect(self.reject)
        buttons = QHBoxLayout()
        buttons.addWidget(save)
        buttons.addWidget(cancel)
        layout = QVBoxLayout(self)
        layout.addLayout(form)
        layout.addLayout(buttons)

from __future__ import annotations

from presentation.framework.application import DesktopApplication
from sigesm.infrastructure.di import ApplicationContainer


def run_qt_application(container: ApplicationContainer) -> int:
    """Run the PySide6 desktop application."""
    return DesktopApplication(container).run()

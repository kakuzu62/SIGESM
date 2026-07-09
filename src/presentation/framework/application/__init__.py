"""Desktop application framework services."""

from presentation.framework.application.application_lifecycle import ApplicationLifecycle
from presentation.framework.application.desktop_application import DesktopApplication
from presentation.framework.application.desktop_context import DesktopContext

__all__ = ["ApplicationLifecycle", "DesktopApplication", "DesktopContext"]

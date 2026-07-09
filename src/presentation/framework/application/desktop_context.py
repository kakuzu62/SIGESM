from __future__ import annotations

from dataclasses import dataclass

from presentation.framework.navigation import NavigationService
from presentation.framework.services import NotificationService
from presentation.framework.themes import ThemeManager
from presentation.framework.workspace import WorkspaceManager


@dataclass(frozen=True, slots=True)
class DesktopContext:
    """Shared services used by the desktop platform."""

    navigation: NavigationService
    workspace: WorkspaceManager
    themes: ThemeManager
    notifications: NotificationService

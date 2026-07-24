from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from presentation.framework.navigation import NavigationService
from presentation.framework.services import NotificationService
from presentation.framework.themes import ThemeManager
from presentation.framework.workspace import WorkspaceManager

if TYPE_CHECKING:
    from presentation.modules.user_management.application import (
        ChangeUserActiveStatusService,
        CreateUserService,
        EditUserService,
        UserListingService,
    )


@dataclass(frozen=True, slots=True)
class DesktopContext:
    """Shared services used by the desktop platform."""

    navigation: NavigationService
    workspace: WorkspaceManager
    themes: ThemeManager
    notifications: NotificationService
    user_listing: UserListingService
    user_creation: CreateUserService
    user_editing: EditUserService
    user_status: ChangeUserActiveStatusService

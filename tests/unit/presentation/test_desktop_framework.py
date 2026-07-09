from __future__ import annotations

from pathlib import Path

from presentation.framework.navigation import NavigationItem, NavigationService
from presentation.framework.resources import ResourceCatalog
from presentation.framework.services import Notification, NotificationService
from presentation.framework.workspace import WorkspaceDocument, WorkspaceManager


def test_navigation_service_tracks_active_route() -> None:
    navigation = NavigationService()
    navigation.register(NavigationItem(key="dashboard", label="Dashboard", route="/dashboard"))

    item = navigation.navigate("dashboard")

    assert item.label == "Dashboard"
    assert navigation.current_route == "/dashboard"


def test_workspace_manager_tracks_documents() -> None:
    workspace = WorkspaceManager()
    workspace.open(WorkspaceDocument(key="dashboard", title="Dashboard", route="/dashboard"))
    workspace.close("missing")

    assert tuple(document.key for document in workspace.documents) == ("dashboard",)


def test_notification_service_stores_notifications() -> None:
    notifications = NotificationService()
    notifications.publish(Notification(title="SIGESM", message="Pronto"))

    assert notifications.items[0].message == "Pronto"


def test_resource_catalog_resolves_paths() -> None:
    catalog = ResourceCatalog(Path("assets"))

    assert catalog.resolve("icons/app.svg") == Path("assets") / "icons/app.svg"

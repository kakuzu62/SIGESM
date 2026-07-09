from __future__ import annotations

from pathlib import Path

from presentation.framework.mvvm import Command, ObservableObject
from presentation.framework.navigation import NavigationHistory, NavigationItem, NavigationService
from presentation.framework.resources import ResourceCatalog
from presentation.framework.services import Notification, NotificationService
from presentation.framework.themes import QssLoader
from presentation.framework.workspace import WorkspaceDocument, WorkspaceManager


def test_navigation_service_tracks_active_route() -> None:
    navigation = NavigationService()
    navigation.register_item(NavigationItem(key="dashboard", title="Dashboard", route="/dashboard"))

    item = navigation.navigate_to("dashboard")

    assert item.title == "Dashboard"
    assert navigation.current_route == "/dashboard"


def test_navigation_history_tracks_back_and_forward() -> None:
    history = NavigationHistory()
    history.record("dashboard")
    history.record("military")

    assert history.back() == "dashboard"
    assert history.forward() == "military"


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


def test_observable_object_notifies_subscribers() -> None:
    observable = ObservableObject()
    changes: list[str] = []
    observable.subscribe(changes.append)

    observable.notify_property_changed("name")

    assert changes == ["name"]


def test_command_executes_when_enabled() -> None:
    executed: list[str] = []
    command = Command(lambda: executed.append("done"), lambda: True)

    command.execute()

    assert executed == ["done"]


def test_qss_loader_returns_empty_when_missing() -> None:
    loader = QssLoader()

    assert loader.load(Path("missing.qss")) == ""

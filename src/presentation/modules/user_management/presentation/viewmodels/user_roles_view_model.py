from __future__ import annotations

from PySide6.QtCore import Signal

from presentation.framework.mvvm import ViewModel
from presentation.modules.user_management.application import (
    AssignUserRolesService,
    ListAvailableRolesService,
)
from presentation.modules.user_management.application.commands.assign_user_roles import (
    AssignUserRolesCommand,
)
from presentation.modules.user_management.application.queries.list_available_roles import (
    RoleListItemDTO,
)
from presentation.modules.user_management.application.queries.list_users import UserListItemDTO


class UserRolesViewModel(ViewModel):
    """ViewModel responsible for assigning roles to a user."""

    roles_loaded = Signal()
    roles_updated = Signal(object)
    update_failed = Signal(str)

    def __init__(
        self,
        actor_user_id: str,
        target_user: UserListItemDTO,
        role_listing: ListAvailableRolesService,
        role_assignment: AssignUserRolesService,
    ) -> None:
        super().__init__()
        self._actor_user_id = actor_user_id
        self._target_user = target_user
        self._role_listing = role_listing
        self._role_assignment = role_assignment
        self._available_roles: tuple[RoleListItemDTO, ...] = ()
        self._original_role_ids: tuple[str, ...] = target_user.role_ids
        self._selected_role_ids: set[str] = set(target_user.role_ids)
        self._field_errors: dict[str, str] = {}
        self._general_error = ""
        self._is_loading = False

    @property
    def target_user_id(self) -> str:
        """Return target user identity."""
        return self._target_user.id

    @property
    def target_user_display_name(self) -> str:
        """Return safe target user label."""
        return f"{self._target_user.name} ({self._target_user.login})"

    @property
    def available_roles(self) -> tuple[RoleListItemDTO, ...]:
        """Return roles available for assignment."""
        return self._available_roles

    @property
    def selected_role_ids(self) -> tuple[str, ...]:
        """Return selected role identities."""
        return tuple(sorted(self._selected_role_ids))

    @property
    def original_role_ids(self) -> tuple[str, ...]:
        """Return originally assigned role identities."""
        return tuple(sorted(self._original_role_ids))

    @property
    def has_changes(self) -> bool:
        """Return whether selected roles differ from original roles."""
        return set(self._original_role_ids) != self._selected_role_ids

    @property
    def is_loading(self) -> bool:
        """Return whether the view model is loading or saving."""
        return self._is_loading

    @property
    def can_submit(self) -> bool:
        """Return whether role assignment can be submitted."""
        return not self._is_loading and self.has_changes

    @property
    def field_errors(self) -> dict[str, str]:
        """Return field errors."""
        return dict(self._field_errors)

    @property
    def general_error(self) -> str:
        """Return general error."""
        return self._general_error

    def load(self) -> None:
        """Load available roles and mark current assignments."""
        if self._is_loading:
            return
        self._set_loading(True)
        try:
            result = self._role_listing.list_roles()
            if result.is_failure:
                self._general_error = result.error
                self.notify_property_changed("general_error")
                self.update_failed.emit(result.error)
                return
            self._available_roles = result.value
            if not self._original_role_ids:
                profile_names = {profile.lower() for profile in self._target_user.profiles}
                inferred = tuple(
                    role.id for role in self._available_roles if role.name.lower() in profile_names
                )
                self._original_role_ids = inferred
                self._selected_role_ids = set(inferred)
            self.notify_property_changed("available_roles")
            self.notify_property_changed("selected_role_ids")
            self.notify_property_changed("original_role_ids")
            self.notify_property_changed("has_changes")
            self.notify_property_changed("can_submit")
            self.roles_loaded.emit()
        finally:
            self._set_loading(False)

    def set_role_selected(self, role_id: str, selected: bool) -> None:
        """Select or unselect one role."""
        if selected:
            self._selected_role_ids.add(role_id)
        else:
            self._selected_role_ids.discard(role_id)
        self.notify_property_changed("selected_role_ids")
        self.notify_property_changed("has_changes")
        self.notify_property_changed("can_submit")

    def submit(self) -> None:
        """Persist the selected role composition."""
        if self._is_loading or not self.has_changes:
            return
        self._field_errors = {}
        self._general_error = ""
        self.notify_property_changed("field_errors")
        self.notify_property_changed("general_error")
        self._set_loading(True)
        try:
            result = self._role_assignment.assign_roles(
                AssignUserRolesCommand(
                    actor_user_id=self._actor_user_id,
                    target_user_id=self._target_user.id,
                    role_ids=tuple(sorted(self._selected_role_ids)),
                )
            )
            if result.is_failure:
                self._general_error = result.error
                self.notify_property_changed("general_error")
                self.update_failed.emit(result.error)
                return
            self._original_role_ids = tuple(sorted(self._selected_role_ids))
            self.notify_property_changed("original_role_ids")
            self.notify_property_changed("has_changes")
            self.notify_property_changed("can_submit")
            self.roles_updated.emit(result.value)
        finally:
            self._set_loading(False)

    def _set_loading(self, is_loading: bool) -> None:
        self._is_loading = is_loading
        self.notify_property_changed("is_loading")
        self.notify_property_changed("can_submit")

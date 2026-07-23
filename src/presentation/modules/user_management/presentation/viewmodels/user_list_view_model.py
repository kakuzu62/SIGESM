from __future__ import annotations

from PySide6.QtCore import Signal

from presentation.framework.mvvm import ViewModel
from presentation.modules.user_management.application import (
    CreateUserService,
    EditUserService,
    UserListingService,
)
from presentation.modules.user_management.application.common import PagedResult, SortDirection
from presentation.modules.user_management.application.commands.create_user import (
    CreateUserResultDTO,
)
from presentation.modules.user_management.application.commands.update_user import (
    UpdateUserResultDTO,
)
from presentation.modules.user_management.application.queries.list_users import (
    ListUsersQuery,
    UserListItemDTO,
)
from presentation.modules.user_management.presentation.viewmodels.create_user_view_model import (
    CreateUserViewModel,
)
from presentation.modules.user_management.presentation.viewmodels.edit_user_view_model import (
    EditUserViewModel,
)


class UserListViewModel(ViewModel):
    """View model for the user listing screen."""

    new_user_requested = Signal()
    edit_user_requested = Signal(object)

    def __init__(
        self,
        service: UserListingService,
        create_user_service: CreateUserService | None = None,
        edit_user_service: EditUserService | None = None,
    ) -> None:
        super().__init__()
        self._service = service
        self._create_user_service = create_user_service
        self._edit_user_service = edit_user_service
        self._query = ListUsersQuery()
        self._result: PagedResult[UserListItemDTO] = PagedResult(
            items=(), total=0, page=1, page_size=20
        )
        self._error_message = ""
        self._is_loading = False

    @property
    def users(self) -> tuple[UserListItemDTO, ...]:
        """Return listed users."""
        return self._result.items

    @property
    def page(self) -> int:
        """Return current page."""
        return self._result.page

    @property
    def total_pages(self) -> int:
        """Return total pages."""
        return self._result.total_pages

    @property
    def total(self) -> int:
        """Return total users."""
        return self._result.total

    @property
    def error_message(self) -> str:
        """Return current error message."""
        return self._error_message

    @property
    def is_loading(self) -> bool:
        """Return whether the view model is currently loading users."""
        return self._is_loading

    def load(self) -> None:
        """Load current query."""
        if self._is_loading:
            return

        self._set_loading(True)
        try:
            result = self._service.list_users(self._query)
            if result.is_success:
                self._result = result.value
                self._error_message = ""
                self._notify_query_state_changed()
                return

            self._error_message = result.error
            self.notify_property_changed("error_message")
        finally:
            self._set_loading(False)

    def refresh(self) -> None:
        """Refresh list."""
        self.load()

    def search(self, text: str) -> None:
        """Search users."""
        self._query = ListUsersQuery(
            page=1,
            page_size=self._query.page_size,
            sort_by=self._query.sort_by,
            direction=self._query.direction,
            filter_text=text,
        )
        self.load()

    def change_page(self, page: int) -> None:
        """Change current page."""
        self._query = ListUsersQuery(
            page=page,
            page_size=self._query.page_size,
            sort_by=self._query.sort_by,
            direction=self._query.direction,
            filter_text=self._query.filter_text,
        )
        self.load()

    def sort(self, sort_by: str) -> None:
        """Sort by a column."""
        direction = (
            SortDirection.DESC
            if self._query.sort_by == sort_by and self._query.direction == SortDirection.ASC
            else SortDirection.ASC
        )
        self._query = ListUsersQuery(
            page=1,
            page_size=self._query.page_size,
            sort_by=sort_by,
            direction=direction,
            filter_text=self._query.filter_text,
        )
        self.load()

    def request_new_user(self) -> None:
        """Request opening the new user form."""
        if self._is_loading or self._create_user_service is None:
            return

        self.new_user_requested.emit()

    def request_edit_user(self, user: UserListItemDTO | None) -> None:
        """Request opening the edit form."""
        if self._is_loading or user is None or self._edit_user_service is None:
            return

        self.edit_user_requested.emit(user)

    def create_user_view_model(self) -> CreateUserViewModel:
        """Create the ViewModel used by the new user dialog."""
        if self._create_user_service is None:
            raise RuntimeError("Create user service is not configured.")
        return CreateUserViewModel(self._create_user_service)

    def edit_user_view_model(self, user: UserListItemDTO) -> EditUserViewModel:
        """Create the ViewModel used by the edit user dialog."""
        if self._edit_user_service is None:
            raise RuntimeError("Edit user service is not configured.")
        return EditUserViewModel(user, self._edit_user_service)

    def handle_user_created(self, user: CreateUserResultDTO) -> None:
        """Refresh the current listing after a user is created."""
        self._error_message = f"Usuario criado: {user.username}"
        self.notify_property_changed("error_message")
        self.refresh()

    def handle_user_updated(self, user: UpdateUserResultDTO) -> None:
        """Refresh the current listing after a user is updated."""
        self._error_message = f"Usuario atualizado: {user.username}"
        self.notify_property_changed("error_message")
        self.refresh()

    def _set_loading(self, is_loading: bool) -> None:
        self._is_loading = is_loading
        self.notify_property_changed("is_loading")

    def _notify_query_state_changed(self) -> None:
        self.notify_property_changed("users")
        self.notify_property_changed("page")
        self.notify_property_changed("total")
        self.notify_property_changed("total_pages")
        self.notify_property_changed("error_message")

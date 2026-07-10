from __future__ import annotations

from presentation.framework.mvvm import ViewModel
from presentation.modules.user_management.application import UserListingService
from presentation.modules.user_management.application.common import PagedResult, SortDirection
from presentation.modules.user_management.application.queries.list_users import (
    ListUsersQuery,
    UserListItemDTO,
)


class UserListViewModel(ViewModel):
    """View model for the user listing screen."""

    def __init__(self, service: UserListingService) -> None:
        super().__init__()
        self._service = service
        self._query = ListUsersQuery()
        self._result: PagedResult[UserListItemDTO] = PagedResult(
            items=(), total=0, page=1, page_size=20
        )
        self._error_message = ""
        self._open_new_requested = False
        self._open_edit_requested: UserListItemDTO | None = None

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
    def open_new_requested(self) -> bool:
        """Return whether opening new user dialog was requested."""
        return self._open_new_requested

    @property
    def open_edit_requested(self) -> UserListItemDTO | None:
        """Return requested edit user."""
        return self._open_edit_requested

    def load(self) -> None:
        """Load current query."""
        result = self._service.list_users(self._query)
        if result.is_success:
            self._result = result.value
            self._error_message = ""
            self.notify_property_changed("users")
            return
        self._error_message = result.error
        self.notify_property_changed("error_message")

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
        self._open_new_requested = True
        self.notify_property_changed("open_new_requested")
        self._open_new_requested = False

    def request_edit_user(self, user: UserListItemDTO | None) -> None:
        """Request opening the edit form."""
        self._open_edit_requested = user
        self.notify_property_changed("open_edit_requested")
        self._open_edit_requested = None

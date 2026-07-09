from __future__ import annotations

from presentation.framework.mvvm import ViewModel
from presentation.modules.user_management.application import UserManagementService
from presentation.modules.user_management.application.commands import (
    ActivateUserCommand,
    CreateUserCommand,
    DeactivateUserCommand,
    ResetPasswordCommand,
    UpdateUserCommand,
)
from presentation.modules.user_management.application.dto import (
    CreateUserDTO,
    UpdateUserDTO,
    UserDTO,
    UserListItemDTO,
)
from presentation.modules.user_management.application.dto.paging import (
    Page,
    UserSearchCriteria,
    UserStatusFilter,
)
from shared.kernel.result import Result


class UserViewModel(ViewModel):
    """View model for user management."""

    def __init__(self, service: UserManagementService, actor_id: str | None = None) -> None:
        super().__init__()
        self._service = service
        self._actor_id = actor_id
        self._criteria = UserSearchCriteria()
        self._page: Page[UserListItemDTO] = Page(items=(), total=0, page=1, page_size=20)
        self._error_message = ""
        self._success_message = ""

    @property
    def users(self) -> tuple[UserListItemDTO, ...]:
        """Return current user table items."""
        return self._page.items

    @property
    def page(self) -> Page[UserListItemDTO]:
        """Return current page."""
        return self._page

    @property
    def error_message(self) -> str:
        """Return last error message."""
        return self._error_message

    @property
    def success_message(self) -> str:
        """Return last success message."""
        return self._success_message

    def load(self) -> None:
        """Load current page."""
        result = self._service.paged_users(self._criteria)
        self._apply_page_result(result)

    def search(self, term: str) -> None:
        """Search users."""
        self._criteria = UserSearchCriteria(
            term=term,
            status=self._criteria.status,
            page=1,
            page_size=self._criteria.page_size,
            sort_by=self._criteria.sort_by,
            direction=self._criteria.direction,
        )
        self.load()

    def filter_status(self, status: str) -> None:
        """Filter users by status."""
        self._criteria = UserSearchCriteria(
            term=self._criteria.term,
            status=UserStatusFilter(status),
            page=1,
            page_size=self._criteria.page_size,
            sort_by=self._criteria.sort_by,
            direction=self._criteria.direction,
        )
        self.load()

    def go_to_page(self, page: int) -> None:
        """Load a specific page."""
        self._criteria = UserSearchCriteria(
            term=self._criteria.term,
            status=self._criteria.status,
            page=page,
            page_size=self._criteria.page_size,
            sort_by=self._criteria.sort_by,
            direction=self._criteria.direction,
        )
        self.load()

    def create_user(self, dto: CreateUserDTO) -> bool:
        """Create a user from form data."""
        result = self._service.create_user(CreateUserCommand(dto, self._actor_id))
        return self._apply_write_result(result, "Usuario criado com sucesso.")

    def update_user(self, dto: UpdateUserDTO) -> bool:
        """Update a user from form data."""
        result = self._service.update_user(UpdateUserCommand(dto, self._actor_id))
        return self._apply_write_result(result, "Usuario atualizado com sucesso.")

    def activate_user(self, user_id: str) -> bool:
        """Activate a user."""
        result = self._service.activate_user(ActivateUserCommand(user_id, self._actor_id))
        return self._apply_write_result(result, "Usuario ativado com sucesso.")

    def deactivate_user(self, user_id: str) -> bool:
        """Deactivate a user."""
        result = self._service.deactivate_user(
            DeactivateUserCommand(user_id, "Desativacao administrativa.", self._actor_id)
        )
        return self._apply_write_result(result, "Usuario desativado com sucesso.")

    def reset_password(self, user_id: str, password: str) -> bool:
        """Reset a user password."""
        result = self._service.reset_password(
            ResetPasswordCommand(user_id, password, self._actor_id)
        )
        return self._apply_write_result(result, "Senha redefinida com sucesso.")

    def _apply_page_result(self, result: Result[Page[UserListItemDTO]]) -> None:
        if result.is_success:
            self._page = result.value
            self._error_message = ""
            self.notify_property_changed("users")
            return
        self._error_message = result.error
        self.notify_property_changed("error_message")

    def _apply_write_result(self, result: Result[UserDTO], success_message: str) -> bool:
        if result.is_failure:
            self._error_message = result.error
            self.notify_property_changed("error_message")
            return False
        self._success_message = success_message
        self.notify_property_changed("success_message")
        self.load()
        return True

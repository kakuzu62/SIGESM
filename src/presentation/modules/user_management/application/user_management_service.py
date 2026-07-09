from __future__ import annotations

from domain.identity.services import PasswordService
from presentation.modules.user_management.application.commands import (
    ActivateUserCommand,
    AssignRoleCommand,
    CreateUserCommand,
    DeactivateUserCommand,
    DeleteUserCommand,
    RemoveRoleCommand,
    ResetPasswordCommand,
    UpdateUserCommand,
)
from presentation.modules.user_management.application.dto import (
    UserDTO,
    UserDetailsDTO,
    UserListItemDTO,
)
from presentation.modules.user_management.application.dto.paging import Page, UserSearchCriteria
from presentation.modules.user_management.application.handlers import (
    ActivateUserHandler,
    AssignRoleHandler,
    CreateUserHandler,
    DeactivateUserHandler,
    DeleteUserHandler,
    GetUserHandler,
    PagedUsersHandler,
    RemoveRoleHandler,
    ResetPasswordHandler,
    UpdateUserHandler,
)
from presentation.modules.user_management.application.queries import GetUserQuery, PagedUsersQuery
from presentation.modules.user_management.application.validators import UserCommandValidator
from presentation.modules.user_management.domain.repositories import IUserManagementRepository
from presentation.modules.user_management.domain.services import UserAuditService
from shared.kernel.result import Result


class UserManagementService:
    """Application facade for user management presentation."""

    def __init__(
        self,
        repository: IUserManagementRepository,
        password_service: PasswordService,
        audit: UserAuditService,
    ) -> None:
        validator = UserCommandValidator(password_service)
        self._create = CreateUserHandler(repository, password_service, validator, audit)
        self._update = UpdateUserHandler(repository, validator, audit)
        self._activate = ActivateUserHandler(repository, audit)
        self._deactivate = DeactivateUserHandler(repository, audit)
        self._reset_password = ResetPasswordHandler(repository, password_service, validator, audit)
        self._assign_role = AssignRoleHandler(repository, audit)
        self._remove_role = RemoveRoleHandler(repository, audit)
        self._delete = DeleteUserHandler(repository, audit)
        self._get = GetUserHandler(repository)
        self._paged = PagedUsersHandler(repository)

    def create_user(self, command: CreateUserCommand) -> Result[UserDTO]:
        """Create a user."""
        return self._create.handle(command)

    def update_user(self, command: UpdateUserCommand) -> Result[UserDTO]:
        """Update a user."""
        return self._update.handle(command)

    def activate_user(self, command: ActivateUserCommand) -> Result[UserDTO]:
        """Activate a user."""
        return self._activate.handle(command)

    def deactivate_user(self, command: DeactivateUserCommand) -> Result[UserDTO]:
        """Deactivate a user."""
        return self._deactivate.handle(command)

    def reset_password(self, command: ResetPasswordCommand) -> Result[UserDTO]:
        """Reset a password."""
        return self._reset_password.handle(command)

    def assign_role(self, command: AssignRoleCommand) -> Result[UserDTO]:
        """Assign a role."""
        return self._assign_role.handle(command)

    def remove_role(self, command: RemoveRoleCommand) -> Result[UserDTO]:
        """Remove a role."""
        return self._remove_role.handle(command)

    def delete_user(self, command: DeleteUserCommand) -> Result[UserDTO]:
        """Soft delete a user."""
        return self._delete.handle(command)

    def get_user(self, query: GetUserQuery) -> Result[UserDetailsDTO]:
        """Return one user."""
        return self._get.handle(query)

    def paged_users(self, criteria: UserSearchCriteria) -> Result[Page[UserListItemDTO]]:
        """Return paged users."""
        return self._paged.handle(PagedUsersQuery(criteria))

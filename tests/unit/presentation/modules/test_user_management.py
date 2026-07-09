from __future__ import annotations

from domain.identity.entities import Role, User
from domain.identity.services import PasswordService
from domain.identity.value_objects import Email, Username
from infrastructure.identity import InMemoryRoleRepository, InMemoryUserRepository
from presentation.modules.user_management.application import UserManagementService
from presentation.modules.user_management.application.commands import (
    ActivateUserCommand,
    CreateUserCommand,
    DeactivateUserCommand,
    ResetPasswordCommand,
)
from presentation.modules.user_management.application.dto import CreateUserDTO
from presentation.modules.user_management.application.dto.paging import UserSearchCriteria
from presentation.modules.user_management.domain.services import UserAuditService
from presentation.modules.user_management.infrastructure.repositories import (
    InMemoryUserManagementRepository,
)
from presentation.modules.user_management.presentation.viewmodels import UserViewModel


def test_create_user_successfully() -> None:
    service = _service()

    result = service.create_user(
        CreateUserCommand(CreateUserDTO("operator", "operator@sigesm.local", "Strong#123"))
    )

    assert result.is_success
    assert result.value.username == "operator"


def test_create_user_rejects_duplicate_username() -> None:
    service = _service()
    dto = CreateUserDTO("operator", "operator@sigesm.local", "Strong#123")
    service.create_user(CreateUserCommand(dto))

    result = service.create_user(
        CreateUserCommand(CreateUserDTO("operator", "other@sigesm.local", "Strong#123"))
    )

    assert result.is_failure
    assert "Username already exists" in result.error


def test_search_users_returns_paged_result() -> None:
    service = _service()
    service.create_user(
        CreateUserCommand(CreateUserDTO("alpha", "alpha@sigesm.local", "Strong#123"))
    )
    service.create_user(
        CreateUserCommand(CreateUserDTO("bravo", "bravo@sigesm.local", "Strong#123"))
    )

    result = service.paged_users(UserSearchCriteria(term="alp", page=1, page_size=10))

    assert result.is_success
    assert tuple(item.username for item in result.value.items) == ("alpha",)


def test_deactivate_last_admin_is_rejected() -> None:
    service = _service(seed_admin=True)
    users = service.paged_users(UserSearchCriteria()).value.items
    admin = next(item for item in users if item.username == "admin")

    result = service.deactivate_user(DeactivateUserCommand(admin.id, "test", "other"))

    assert result.is_failure
    assert "last administrator" in result.error


def test_reset_password_requires_strong_password() -> None:
    service = _service()
    created = service.create_user(
        CreateUserCommand(CreateUserDTO("operator", "operator@sigesm.local", "Strong#123"))
    ).value

    result = service.reset_password(ResetPasswordCommand(created.id, "weak"))

    assert result.is_failure


def test_user_view_model_loads_users() -> None:
    service = _service()
    service.create_user(
        CreateUserCommand(CreateUserDTO("operator", "operator@sigesm.local", "Strong#123"))
    )
    view_model = UserViewModel(service)

    view_model.load()

    assert view_model.users[0].username == "operator"


def test_activate_user_successfully() -> None:
    service = _service()
    created = service.create_user(
        CreateUserCommand(CreateUserDTO("operator", "operator@sigesm.local", "Strong#123"))
    ).value
    service.deactivate_user(DeactivateUserCommand(created.id, "test", "admin"))

    result = service.activate_user(ActivateUserCommand(created.id))

    assert result.is_success
    assert result.value.active


def _service(seed_admin: bool = False) -> UserManagementService:
    users = InMemoryUserRepository()
    roles = InMemoryRoleRepository()
    admin_role = roles.add(Role.create("admin", "Administrator"))
    if seed_admin:
        password_service = PasswordService()
        admin = User.create(
            Username("admin"),
            Email("admin@sigesm.local"),
            password_service.hash_password("Admin#123"),
        )
        admin.assign_role(admin_role)
        users.add(admin)
    password_service = PasswordService()
    repository = InMemoryUserManagementRepository(users, roles)
    return UserManagementService(repository, password_service, UserAuditService())

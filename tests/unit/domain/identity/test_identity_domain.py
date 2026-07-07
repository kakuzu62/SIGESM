from __future__ import annotations

from collections.abc import Sequence

import pytest

from application.identity.commands import (
    ActivateUserCommand,
    ActivateUserHandler,
    ChangePasswordCommand,
    ChangePasswordHandler,
    CreateUserCommand,
    CreateUserHandler,
    DeactivateUserCommand,
    DeactivateUserHandler,
)
from application.identity.queries import (
    GetUserByIdHandler,
    GetUserByIdQuery,
    ListUsersHandler,
    ListUsersQuery,
)
from domain.identity.entities import Permission, Role, User
from domain.identity.events import PasswordChanged, UserActivated, UserCreated, UserDeactivated
from domain.identity.exceptions import InvalidPasswordException
from domain.identity.policies import LoginAttemptPolicy, PasswordPolicy
from domain.identity.repositories import IUserRepository
from domain.identity.services import PasswordService, PermissionService
from domain.identity.value_objects import Email, PermissionCode, Username
from shared.kernel.identity import Identity


class InMemoryUserRepository(IUserRepository):
    """In-memory user repository used by application tests."""

    def __init__(self) -> None:
        self._users: dict[Identity, User] = {}

    def add(self, entity: User) -> User:
        self._users[entity.id] = entity
        return entity

    def update(self, entity: User) -> User:
        self._users[entity.id] = entity
        return entity

    def delete(self, entity: User) -> None:
        self._users.pop(entity.id, None)

    def get_by_id(self, entity_id: Identity) -> User | None:
        return self._users.get(entity_id)

    def get_by_username(self, username: Username) -> User | None:
        return next((user for user in self._users.values() if user.username == username), None)

    def get_by_email(self, email: Email) -> User | None:
        return next((user for user in self._users.values() if user.email == email), None)

    def exists(self, entity_id: Identity) -> bool:
        return entity_id in self._users

    def count(self) -> int:
        return len(self._users)

    def list(self) -> Sequence[User]:
        return tuple(self._users.values())

    def first(self) -> User | None:
        return next(iter(self._users.values()), None)


def test_user_creation_hashes_password_and_emits_event() -> None:
    password_service = PasswordService()
    user = User.create(
        Username("Admin.User"),
        Email("ADMIN@SIGESM.local"),
        password_service.hash_password("Strong#123"),
    )

    events = user.pull_domain_events()

    assert user.username.value == "admin.user"
    assert user.email.value == "admin@sigesm.local"
    assert "Strong#123" not in user.password_hash.value
    assert password_service.verify("Strong#123", user.password_hash)
    assert isinstance(events[0], UserCreated)


def test_password_policy_rejects_weak_password() -> None:
    with pytest.raises(InvalidPasswordException):
        PasswordPolicy().validate("weak")


def test_role_permission_assignment_and_permission_service() -> None:
    permission = Permission.create(PermissionCode("IDENTITY.USER.CREATE"), "Create users")
    role = Role.create("Administrator")
    role.add_permission(permission)
    user = User.create(
        Username("operator"),
        Email("operator@sigesm.local"),
        PasswordService().hash_password("Strong#123"),
    )
    user.assign_role(role)

    assert PermissionService().has_permission(user, PermissionCode("identity:user:create"))


def test_user_lifecycle_events() -> None:
    user = User.create(
        Username("security"),
        Email("security@sigesm.local"),
        PasswordService().hash_password("Strong#123"),
    )
    user.pull_domain_events()

    user.deactivate("security review")
    user.activate()
    user.change_password(PasswordService().hash_password("Better#123"))
    events = user.pull_domain_events()

    assert isinstance(events[0], UserDeactivated)
    assert isinstance(events[1], UserActivated)
    assert isinstance(events[2], PasswordChanged)


def test_login_attempt_policy_locks_after_threshold() -> None:
    user = User.create(
        Username("locked"),
        Email("locked@sigesm.local"),
        PasswordService().hash_password("Strong#123"),
    )
    policy = LoginAttemptPolicy(max_attempts=2, lock_minutes=10)

    policy.register_failure(user)
    policy.register_failure(user)

    assert user.locked_until is not None
    assert not policy.can_attempt_login(user)


def test_identity_application_handlers() -> None:
    repository = InMemoryUserRepository()
    password_service = PasswordService()

    created = CreateUserHandler(repository, password_service).handle(
        CreateUserCommand("manager", "manager@sigesm.local", "Strong#123")
    )
    DeactivateUserHandler(repository).handle(DeactivateUserCommand(created.id, "rotation"))
    inactive = GetUserByIdHandler(repository).handle(GetUserByIdQuery(created.id))
    ActivateUserHandler(repository).handle(ActivateUserCommand(created.id))
    changed = ChangePasswordHandler(repository, password_service).handle(
        ChangePasswordCommand(created.id, "Better#123")
    )
    users = ListUsersHandler(repository).handle(ListUsersQuery(include_inactive=False))

    assert inactive is not None
    assert inactive.active is False
    assert changed.active is True
    assert tuple(user.username for user in users) == ("manager",)

from __future__ import annotations

from collections.abc import Sequence
from datetime import timedelta

import pytest
from argon2 import PasswordHasher

from domain.identity.entities import (
    AuthenticationAttempt,
    AuthenticationSession,
    PasswordResetRequest,
    RefreshSession,
    User,
)
from domain.identity.exceptions import IdentityDomainException
from domain.identity.policies import LoginAttemptPolicy
from domain.identity.repositories import (
    IAuthenticationAttemptRepository,
    IAuthenticationSessionRepository,
    IPasswordResetRequestRepository,
    IRefreshSessionRepository,
    IUserRepository,
)
from domain.identity.services import AuthenticationService, PasswordService
from domain.identity.value_objects import Email, Username
from shared.kernel.identity import Identity


class InMemoryUserRepository(IUserRepository):
    """In-memory user repository for authentication tests."""

    def __init__(self) -> None:
        self.items: dict[Identity, User] = {}

    def add(self, entity: User) -> User:
        self.items[entity.id] = entity
        return entity

    def update(self, entity: User) -> User:
        self.items[entity.id] = entity
        return entity

    def delete(self, entity: User) -> None:
        self.items.pop(entity.id, None)

    def get_by_id(self, entity_id: Identity) -> User | None:
        return self.items.get(entity_id)

    def get_by_username(self, username: Username) -> User | None:
        return next((user for user in self.items.values() if user.username == username), None)

    def get_by_email(self, email: Email) -> User | None:
        return next((user for user in self.items.values() if user.email == email), None)

    def exists(self, entity_id: Identity) -> bool:
        return entity_id in self.items

    def count(self) -> int:
        return len(self.items)

    def list(self) -> Sequence[User]:
        return tuple(self.items.values())

    def first(self) -> User | None:
        return next(iter(self.items.values()), None)


class InMemoryAuthenticationSessionRepository(IAuthenticationSessionRepository):
    """In-memory authentication session repository."""

    def __init__(self) -> None:
        self.items: dict[Identity, AuthenticationSession] = {}

    def add(self, entity: AuthenticationSession) -> AuthenticationSession:
        self.items[entity.id] = entity
        return entity

    def update(self, entity: AuthenticationSession) -> AuthenticationSession:
        self.items[entity.id] = entity
        return entity

    def delete(self, entity: AuthenticationSession) -> None:
        self.items.pop(entity.id, None)

    def get_by_id(self, entity_id: Identity) -> AuthenticationSession | None:
        return self.items.get(entity_id)

    def get_by_token_hash(self, token_hash: str) -> AuthenticationSession | None:
        return next((item for item in self.items.values() if item.token_hash == token_hash), None)

    def list_active_by_user(self, user_id: Identity) -> tuple[AuthenticationSession, ...]:
        return tuple(
            item for item in self.items.values() if item.user_id == user_id and item.active
        )

    def exists(self, entity_id: Identity) -> bool:
        return entity_id in self.items

    def count(self) -> int:
        return len(self.items)

    def list(self) -> Sequence[AuthenticationSession]:
        return tuple(self.items.values())

    def first(self) -> AuthenticationSession | None:
        return next(iter(self.items.values()), None)


class InMemoryRefreshSessionRepository(IRefreshSessionRepository):
    """In-memory refresh session repository."""

    def __init__(self) -> None:
        self.items: dict[Identity, RefreshSession] = {}

    def add(self, entity: RefreshSession) -> RefreshSession:
        self.items[entity.id] = entity
        return entity

    def update(self, entity: RefreshSession) -> RefreshSession:
        self.items[entity.id] = entity
        return entity

    def delete(self, entity: RefreshSession) -> None:
        self.items.pop(entity.id, None)

    def get_by_id(self, entity_id: Identity) -> RefreshSession | None:
        return self.items.get(entity_id)

    def get_by_token_hash(self, token_hash: str) -> RefreshSession | None:
        return next((item for item in self.items.values() if item.token_hash == token_hash), None)

    def exists(self, entity_id: Identity) -> bool:
        return entity_id in self.items

    def count(self) -> int:
        return len(self.items)

    def list(self) -> Sequence[RefreshSession]:
        return tuple(self.items.values())

    def first(self) -> RefreshSession | None:
        return next(iter(self.items.values()), None)


class InMemoryPasswordResetRepository(IPasswordResetRequestRepository):
    """In-memory password reset repository."""

    def __init__(self) -> None:
        self.items: dict[Identity, PasswordResetRequest] = {}

    def add(self, entity: PasswordResetRequest) -> PasswordResetRequest:
        self.items[entity.id] = entity
        return entity

    def update(self, entity: PasswordResetRequest) -> PasswordResetRequest:
        self.items[entity.id] = entity
        return entity

    def delete(self, entity: PasswordResetRequest) -> None:
        self.items.pop(entity.id, None)

    def get_by_id(self, entity_id: Identity) -> PasswordResetRequest | None:
        return self.items.get(entity_id)

    def get_by_token_hash(self, token_hash: str) -> PasswordResetRequest | None:
        return next((item for item in self.items.values() if item.token_hash == token_hash), None)

    def get_active_by_user(self, user_id: Identity) -> PasswordResetRequest | None:
        return next(
            (item for item in self.items.values() if item.user_id == user_id and item.active), None
        )

    def exists(self, entity_id: Identity) -> bool:
        return entity_id in self.items

    def count(self) -> int:
        return len(self.items)

    def list(self) -> Sequence[PasswordResetRequest]:
        return tuple(self.items.values())

    def first(self) -> PasswordResetRequest | None:
        return next(iter(self.items.values()), None)


class InMemoryAuthenticationAttemptRepository(IAuthenticationAttemptRepository):
    """In-memory authentication attempt repository."""

    def __init__(self) -> None:
        self.items: dict[Identity, AuthenticationAttempt] = {}

    def add(self, entity: AuthenticationAttempt) -> AuthenticationAttempt:
        self.items[entity.id] = entity
        return entity

    def update(self, entity: AuthenticationAttempt) -> AuthenticationAttempt:
        self.items[entity.id] = entity
        return entity

    def delete(self, entity: AuthenticationAttempt) -> None:
        self.items.pop(entity.id, None)

    def get_by_id(self, entity_id: Identity) -> AuthenticationAttempt | None:
        return self.items.get(entity_id)

    def exists(self, entity_id: Identity) -> bool:
        return entity_id in self.items

    def count(self) -> int:
        return len(self.items)

    def list(self) -> Sequence[AuthenticationAttempt]:
        return tuple(self.items.values())

    def first(self) -> AuthenticationAttempt | None:
        return next(iter(self.items.values()), None)


def password_service() -> PasswordService:
    """Return a fast Argon2id password service for tests."""
    return PasswordService(
        password_hasher=PasswordHasher(time_cost=1, memory_cost=1024, parallelism=1)
    )


def authentication_service(
    session_duration: timedelta = timedelta(hours=8),
    login_policy: LoginAttemptPolicy | None = None,
) -> tuple[AuthenticationService, InMemoryUserRepository, InMemoryAuthenticationSessionRepository]:
    """Build an authentication service with in-memory dependencies."""
    users = InMemoryUserRepository()
    sessions = InMemoryAuthenticationSessionRepository()
    auth = AuthenticationService(
        users=users,
        sessions=sessions,
        refresh_sessions=InMemoryRefreshSessionRepository(),
        password_resets=InMemoryPasswordResetRepository(),
        attempts=InMemoryAuthenticationAttemptRepository(),
        password_service=password_service(),
        login_attempt_policy=login_policy,
        session_duration=session_duration,
    )
    user = User.create(
        Username("operator"),
        Email("operator@sigesm.local"),
        password_service().hash_password("Strong#123"),
    )
    users.add(user)
    return auth, users, sessions


def test_valid_login_creates_session() -> None:
    auth, _users, _sessions = authentication_service()

    tokens = auth.authenticate(Username("operator"), "Strong#123")

    assert auth.validate_session(tokens.access_token) is not None


def test_invalid_password_records_failure() -> None:
    auth, users, _sessions = authentication_service()

    with pytest.raises(IdentityDomainException):
        auth.authenticate(Username("operator"), "Wrong#123")

    user = users.get_by_username(Username("operator"))
    assert user is not None
    assert user.failed_login_attempts == 1


def test_blocked_user_cannot_login() -> None:
    auth, _users, _sessions = authentication_service(
        login_policy=LoginAttemptPolicy(max_attempts=1)
    )

    with pytest.raises(IdentityDomainException):
        auth.authenticate(Username("operator"), "Wrong#123")
    with pytest.raises(IdentityDomainException):
        auth.authenticate(Username("operator"), "Strong#123")


def test_expired_session_is_not_valid() -> None:
    auth, _users, _sessions = authentication_service(session_duration=timedelta(seconds=-1))
    tokens = auth.authenticate(Username("operator"), "Strong#123")

    assert auth.validate_session(tokens.access_token) is None


def test_change_password_requires_current_password() -> None:
    auth, _users, _sessions = authentication_service()

    auth.change_password(Username("operator"), "Strong#123", "Better#123")
    tokens = auth.authenticate(Username("operator"), "Better#123")

    assert auth.validate_session(tokens.access_token) is not None


def test_password_reset_changes_password() -> None:
    auth, _users, _sessions = authentication_service()

    reset_token, request = auth.request_password_reset(Email("operator@sigesm.local"))
    auth.confirm_password_reset(reset_token, "Better#123")

    assert request.used_at is not None
    assert auth.authenticate(Username("operator"), "Better#123") is not None


def test_renew_session_revokes_previous_session() -> None:
    auth, _users, sessions = authentication_service()
    tokens = auth.authenticate(Username("operator"), "Strong#123")

    renewed = auth.renew_session(tokens.refresh_token)

    assert auth.validate_session(tokens.access_token) is None
    assert auth.validate_session(renewed.access_token) is not None
    assert sessions.count() == 2

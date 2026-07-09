from __future__ import annotations

from collections.abc import Sequence

from domain.identity.entities import (
    AuthenticationAttempt,
    AuthenticationSession,
    PasswordResetRequest,
    RefreshSession,
    User,
)
from domain.identity.repositories import (
    IAuthenticationAttemptRepository,
    IAuthenticationSessionRepository,
    IPasswordResetRequestRepository,
    IRefreshSessionRepository,
    IUserRepository,
)
from domain.identity.value_objects import Email, Username
from shared.kernel.identity import Identity


class InMemoryUserRepository(IUserRepository):
    """In-memory user repository for local desktop bootstrap."""

    def __init__(self) -> None:
        self._items: dict[Identity, User] = {}

    def add(self, entity: User) -> User:
        self._items[entity.id] = entity
        return entity

    def update(self, entity: User) -> User:
        self._items[entity.id] = entity
        return entity

    def delete(self, entity: User) -> None:
        self._items.pop(entity.id, None)

    def get_by_id(self, entity_id: Identity) -> User | None:
        return self._items.get(entity_id)

    def get_by_username(self, username: Username) -> User | None:
        return next((user for user in self._items.values() if user.username == username), None)

    def get_by_email(self, email: Email) -> User | None:
        return next((user for user in self._items.values() if user.email == email), None)

    def exists(self, entity_id: Identity) -> bool:
        return entity_id in self._items

    def count(self) -> int:
        return len(self._items)

    def list(self) -> Sequence[User]:
        return tuple(self._items.values())

    def first(self) -> User | None:
        return next(iter(self._items.values()), None)


class InMemoryAuthenticationSessionRepository(IAuthenticationSessionRepository):
    """In-memory authentication session repository."""

    def __init__(self) -> None:
        self._items: dict[Identity, AuthenticationSession] = {}

    def add(self, entity: AuthenticationSession) -> AuthenticationSession:
        self._items[entity.id] = entity
        return entity

    def update(self, entity: AuthenticationSession) -> AuthenticationSession:
        self._items[entity.id] = entity
        return entity

    def delete(self, entity: AuthenticationSession) -> None:
        self._items.pop(entity.id, None)

    def get_by_id(self, entity_id: Identity) -> AuthenticationSession | None:
        return self._items.get(entity_id)

    def get_by_token_hash(self, token_hash: str) -> AuthenticationSession | None:
        return next((item for item in self._items.values() if item.token_hash == token_hash), None)

    def list_active_by_user(self, user_id: Identity) -> tuple[AuthenticationSession, ...]:
        return tuple(
            item for item in self._items.values() if item.user_id == user_id and item.active
        )

    def exists(self, entity_id: Identity) -> bool:
        return entity_id in self._items

    def count(self) -> int:
        return len(self._items)

    def list(self) -> Sequence[AuthenticationSession]:
        return tuple(self._items.values())

    def first(self) -> AuthenticationSession | None:
        return next(iter(self._items.values()), None)


class InMemoryRefreshSessionRepository(IRefreshSessionRepository):
    """In-memory refresh session repository."""

    def __init__(self) -> None:
        self._items: dict[Identity, RefreshSession] = {}

    def add(self, entity: RefreshSession) -> RefreshSession:
        self._items[entity.id] = entity
        return entity

    def update(self, entity: RefreshSession) -> RefreshSession:
        self._items[entity.id] = entity
        return entity

    def delete(self, entity: RefreshSession) -> None:
        self._items.pop(entity.id, None)

    def get_by_id(self, entity_id: Identity) -> RefreshSession | None:
        return self._items.get(entity_id)

    def get_by_token_hash(self, token_hash: str) -> RefreshSession | None:
        return next((item for item in self._items.values() if item.token_hash == token_hash), None)

    def exists(self, entity_id: Identity) -> bool:
        return entity_id in self._items

    def count(self) -> int:
        return len(self._items)

    def list(self) -> Sequence[RefreshSession]:
        return tuple(self._items.values())

    def first(self) -> RefreshSession | None:
        return next(iter(self._items.values()), None)


class InMemoryPasswordResetRequestRepository(IPasswordResetRequestRepository):
    """In-memory password reset request repository."""

    def __init__(self) -> None:
        self._items: dict[Identity, PasswordResetRequest] = {}

    def add(self, entity: PasswordResetRequest) -> PasswordResetRequest:
        self._items[entity.id] = entity
        return entity

    def update(self, entity: PasswordResetRequest) -> PasswordResetRequest:
        self._items[entity.id] = entity
        return entity

    def delete(self, entity: PasswordResetRequest) -> None:
        self._items.pop(entity.id, None)

    def get_by_id(self, entity_id: Identity) -> PasswordResetRequest | None:
        return self._items.get(entity_id)

    def get_by_token_hash(self, token_hash: str) -> PasswordResetRequest | None:
        return next((item for item in self._items.values() if item.token_hash == token_hash), None)

    def get_active_by_user(self, user_id: Identity) -> PasswordResetRequest | None:
        return next(
            (item for item in self._items.values() if item.user_id == user_id and item.active), None
        )

    def exists(self, entity_id: Identity) -> bool:
        return entity_id in self._items

    def count(self) -> int:
        return len(self._items)

    def list(self) -> Sequence[PasswordResetRequest]:
        return tuple(self._items.values())

    def first(self) -> PasswordResetRequest | None:
        return next(iter(self._items.values()), None)


class InMemoryAuthenticationAttemptRepository(IAuthenticationAttemptRepository):
    """In-memory authentication attempt repository."""

    def __init__(self) -> None:
        self._items: dict[Identity, AuthenticationAttempt] = {}

    def add(self, entity: AuthenticationAttempt) -> AuthenticationAttempt:
        self._items[entity.id] = entity
        return entity

    def update(self, entity: AuthenticationAttempt) -> AuthenticationAttempt:
        self._items[entity.id] = entity
        return entity

    def delete(self, entity: AuthenticationAttempt) -> None:
        self._items.pop(entity.id, None)

    def get_by_id(self, entity_id: Identity) -> AuthenticationAttempt | None:
        return self._items.get(entity_id)

    def exists(self, entity_id: Identity) -> bool:
        return entity_id in self._items

    def count(self) -> int:
        return len(self._items)

    def list(self) -> Sequence[AuthenticationAttempt]:
        return tuple(self._items.values())

    def first(self) -> AuthenticationAttempt | None:
        return next(iter(self._items.values()), None)

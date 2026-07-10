from __future__ import annotations

from dataclasses import dataclass
from functools import cached_property

from application.identity.commands import AuthenticateUserHandler
from domain.identity.entities import User
from domain.identity.policies import LoginAttemptPolicy
from domain.identity.services import AuthenticationService, PasswordService
from domain.identity.value_objects import Email, Username
from infrastructure.identity import (
    InMemoryAuthenticationAttemptRepository,
    InMemoryAuthenticationSessionRepository,
    InMemoryPasswordResetRequestRepository,
    InMemoryRefreshSessionRepository,
    InMemoryUserRepository,
)
from presentation.modules.user_management.application import UserListingService
from presentation.modules.user_management.infrastructure.repositories import (
    InMemoryUserListingRepository,
)
from sigesm.application.ports import UnitOfWorkFactory
from sigesm.application.use_cases import RunHealthCheck
from sigesm.config.settings import Settings
from sigesm.infrastructure.database.session import DatabaseSessionFactory


@dataclass(frozen=True, kw_only=True)
class ApplicationContainer:
    settings: Settings
    session_factory: DatabaseSessionFactory
    unit_of_work_factory: UnitOfWorkFactory

    def health_check(self) -> RunHealthCheck:
        return RunHealthCheck(unit_of_work_factory=self.unit_of_work_factory)

    @cached_property
    def password_service(self) -> PasswordService:
        """Return the shared password service."""
        return PasswordService()

    @cached_property
    def identity_users(self) -> InMemoryUserRepository:
        """Return shared local users for desktop bootstrap."""
        users = InMemoryUserRepository()
        users.add(
            User.create(
                Username("admin"),
                Email("admin@sigesm.local"),
                self.password_service.hash_password("Admin#123"),
            )
        )
        return users

    def authentication_service(self) -> AuthenticationService:
        """Build the desktop authentication service."""
        return AuthenticationService(
            users=self.identity_users,
            sessions=InMemoryAuthenticationSessionRepository(),
            refresh_sessions=InMemoryRefreshSessionRepository(),
            password_resets=InMemoryPasswordResetRequestRepository(),
            attempts=InMemoryAuthenticationAttemptRepository(),
            password_service=self.password_service,
            login_attempt_policy=LoginAttemptPolicy(max_attempts=5, lock_minutes=15),
        )

    def authenticate_user_handler(self) -> AuthenticateUserHandler:
        """Return the authenticate user use case handler."""
        return AuthenticateUserHandler(self.authentication_service())

    def user_listing_service(self) -> UserListingService:
        """Return the user listing application facade."""
        return UserListingService(InMemoryUserListingRepository(self.identity_users))

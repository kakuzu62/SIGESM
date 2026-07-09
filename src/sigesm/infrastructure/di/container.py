from __future__ import annotations

from dataclasses import dataclass

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

    def authentication_service(self) -> AuthenticationService:
        """Build the desktop authentication service."""
        users = InMemoryUserRepository()
        password_service = PasswordService()
        users.add(
            User.create(
                Username("admin"),
                Email("admin@sigesm.local"),
                password_service.hash_password("Admin#123"),
            )
        )
        return AuthenticationService(
            users=users,
            sessions=InMemoryAuthenticationSessionRepository(),
            refresh_sessions=InMemoryRefreshSessionRepository(),
            password_resets=InMemoryPasswordResetRequestRepository(),
            attempts=InMemoryAuthenticationAttemptRepository(),
            password_service=password_service,
            login_attempt_policy=LoginAttemptPolicy(max_attempts=5, lock_minutes=15),
        )

    def authenticate_user_handler(self) -> AuthenticateUserHandler:
        """Return the authenticate user use case handler."""
        return AuthenticateUserHandler(self.authentication_service())

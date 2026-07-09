from __future__ import annotations

from dataclasses import dataclass
from functools import cached_property

from application.identity.commands import AuthenticateUserHandler
from domain.identity.entities import Role, User
from domain.identity.policies import LoginAttemptPolicy
from domain.identity.services import AuthenticationService, PasswordService
from domain.identity.value_objects import Email, Username
from infrastructure.identity import (
    InMemoryAuthenticationAttemptRepository,
    InMemoryAuthenticationSessionRepository,
    InMemoryPasswordResetRequestRepository,
    InMemoryRefreshSessionRepository,
    InMemoryRoleRepository,
    InMemoryUserRepository,
)
from presentation.modules.user_management.application import UserManagementService
from presentation.modules.user_management.domain.services import UserAuditService
from presentation.modules.user_management.infrastructure.repositories import (
    InMemoryUserManagementRepository,
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
        """Return the shared desktop user repository."""
        users = InMemoryUserRepository()
        admin = User.create(
            Username("admin"),
            Email("admin@sigesm.local"),
            self.password_service.hash_password("Admin#123"),
        )
        admin_role = self.identity_roles.get_by_name("admin")
        if admin_role is not None:
            admin.assign_role(admin_role)
        users.add(admin)
        return users

    @cached_property
    def identity_roles(self) -> InMemoryRoleRepository:
        """Return the shared desktop role repository."""
        roles = InMemoryRoleRepository()
        roles.add(Role.create("admin", "Administrador do sistema"))
        roles.add(Role.create("operator", "Operador do sistema"))
        return roles

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

    def user_management_service(self) -> UserManagementService:
        """Return the user management application facade."""
        repository = InMemoryUserManagementRepository(self.identity_users, self.identity_roles)
        return UserManagementService(repository, self.password_service, UserAuditService())

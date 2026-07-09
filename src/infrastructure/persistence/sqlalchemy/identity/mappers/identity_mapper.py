from __future__ import annotations

from domain.identity.entities import (
    AuthenticationAttempt,
    AuthenticationSession,
    PasswordResetRequest,
    Permission,
    RefreshSession,
    Role,
    User,
    UserSession,
)
from domain.identity.value_objects import (
    Email,
    PasswordHash,
    PermissionCode,
    SessionStatus,
    Username,
)
from infrastructure.persistence.sqlalchemy.identity.models import (
    AuthenticationAttemptModel,
    AuthenticationSessionModel,
    PasswordResetRequestModel,
    PermissionModel,
    RefreshSessionModel,
    RoleModel,
    UserModel,
    UserSessionModel,
)
from shared.kernel.identity import Identity


class IdentityMapper:
    """Maps identity domain objects to SQLAlchemy models and back."""

    @staticmethod
    def permission_to_domain(model: PermissionModel) -> Permission:
        """Map a permission model to a domain entity."""
        return Permission(
            entity_id=Identity.from_string(model.id),
            code=PermissionCode(model.code),
            description=model.description,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )

    @classmethod
    def role_to_domain(cls, model: RoleModel) -> Role:
        """Map a role model to a domain entity."""
        return Role(
            entity_id=Identity.from_string(model.id),
            name=model.name,
            description=model.description,
            permissions=tuple(
                cls.permission_to_domain(permission) for permission in model.permissions
            ),
            created_at=model.created_at,
            updated_at=model.updated_at,
        )

    @classmethod
    def user_to_domain(cls, model: UserModel) -> User:
        """Map a user model to a domain aggregate."""
        return User(
            entity_id=Identity.from_string(model.id),
            username=Username(model.username),
            email=Email(model.email),
            password_hash=PasswordHash(model.password_hash),
            roles=tuple(cls.role_to_domain(role) for role in model.roles),
            active=model.active,
            failed_login_attempts=model.failed_login_attempts,
            locked_until=model.locked_until,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )

    @staticmethod
    def session_to_domain(model: UserSessionModel) -> UserSession:
        """Map a user session model to a domain entity."""
        return UserSession(
            entity_id=Identity.from_string(model.id),
            user_id=Identity.from_string(model.user_id),
            status=SessionStatus(model.status),
            created_at=model.created_at,
            expires_at=model.expires_at,
            ended_at=model.ended_at,
        )

    @staticmethod
    def authentication_session_to_domain(
        model: AuthenticationSessionModel,
    ) -> AuthenticationSession:
        """Map an authentication session model to a domain entity."""
        return AuthenticationSession(
            entity_id=Identity.from_string(model.id),
            user_id=Identity.from_string(model.user_id),
            token_hash=model.token_hash,
            status=SessionStatus(model.status),
            created_at=model.created_at,
            expires_at=model.expires_at,
            revoked_at=model.revoked_at,
        )

    @staticmethod
    def refresh_session_to_domain(model: RefreshSessionModel) -> RefreshSession:
        """Map a refresh session model to a domain entity."""
        return RefreshSession(
            entity_id=Identity.from_string(model.id),
            user_id=Identity.from_string(model.user_id),
            session_id=Identity.from_string(model.session_id),
            token_hash=model.token_hash,
            created_at=model.created_at,
            expires_at=model.expires_at,
            revoked_at=model.revoked_at,
        )

    @staticmethod
    def password_reset_to_domain(model: PasswordResetRequestModel) -> PasswordResetRequest:
        """Map a password reset model to a domain entity."""
        return PasswordResetRequest(
            entity_id=Identity.from_string(model.id),
            user_id=Identity.from_string(model.user_id),
            token_hash=model.token_hash,
            created_at=model.created_at,
            expires_at=model.expires_at,
            used_at=model.used_at,
        )

    @staticmethod
    def authentication_attempt_to_domain(
        model: AuthenticationAttemptModel,
    ) -> AuthenticationAttempt:
        """Map an authentication attempt model to a domain entity."""
        return AuthenticationAttempt(
            entity_id=Identity.from_string(model.id),
            username=Username(model.username),
            successful=model.successful,
            reason=model.reason,
            occurred_at=model.occurred_at,
        )

    @staticmethod
    def permission_to_model(entity: Permission) -> PermissionModel:
        """Map a permission entity to a SQLAlchemy model."""
        return PermissionModel(
            id=str(entity.id),
            code=entity.code.value,
            description=entity.description,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )

    @classmethod
    def role_to_model(cls, entity: Role) -> RoleModel:
        """Map a role entity to a SQLAlchemy model."""
        model = RoleModel(
            id=str(entity.id),
            name=entity.name,
            description=entity.description,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )
        model.permissions = [
            cls.permission_to_model(permission) for permission in entity.permissions
        ]
        return model

    @classmethod
    def user_to_model(cls, entity: User) -> UserModel:
        """Map a user aggregate to a SQLAlchemy model."""
        model = UserModel(
            id=str(entity.id),
            username=entity.username.value,
            email=entity.email.value,
            password_hash=entity.password_hash.value,
            active=entity.active,
            failed_login_attempts=entity.failed_login_attempts,
            locked_until=entity.locked_until,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )
        model.roles = [cls.role_to_model(role) for role in entity.roles]
        return model

    @staticmethod
    def session_to_model(entity: UserSession) -> UserSessionModel:
        """Map a user session entity to a SQLAlchemy model."""
        return UserSessionModel(
            id=str(entity.id),
            user_id=str(entity.user_id),
            status=entity.status.value,
            created_at=entity.created_at,
            expires_at=entity.expires_at,
            ended_at=entity.ended_at,
        )

    @staticmethod
    def authentication_session_to_model(
        entity: AuthenticationSession,
    ) -> AuthenticationSessionModel:
        """Map an authentication session entity to a SQLAlchemy model."""
        return AuthenticationSessionModel(
            id=str(entity.id),
            user_id=str(entity.user_id),
            token_hash=entity.token_hash,
            status=entity.status.value,
            created_at=entity.created_at,
            expires_at=entity.expires_at,
            revoked_at=entity.revoked_at,
        )

    @staticmethod
    def refresh_session_to_model(entity: RefreshSession) -> RefreshSessionModel:
        """Map a refresh session entity to a SQLAlchemy model."""
        return RefreshSessionModel(
            id=str(entity.id),
            user_id=str(entity.user_id),
            session_id=str(entity.session_id),
            token_hash=entity.token_hash,
            created_at=entity.created_at,
            expires_at=entity.expires_at,
            revoked_at=entity.revoked_at,
        )

    @staticmethod
    def password_reset_to_model(entity: PasswordResetRequest) -> PasswordResetRequestModel:
        """Map a password reset request entity to a SQLAlchemy model."""
        return PasswordResetRequestModel(
            id=str(entity.id),
            user_id=str(entity.user_id),
            token_hash=entity.token_hash,
            created_at=entity.created_at,
            expires_at=entity.expires_at,
            used_at=entity.used_at,
        )

    @staticmethod
    def authentication_attempt_to_model(
        entity: AuthenticationAttempt,
    ) -> AuthenticationAttemptModel:
        """Map an authentication attempt entity to a SQLAlchemy model."""
        return AuthenticationAttemptModel(
            id=str(entity.id),
            username=entity.username.value,
            successful=entity.successful,
            reason=entity.reason,
            occurred_at=entity.occurred_at,
        )

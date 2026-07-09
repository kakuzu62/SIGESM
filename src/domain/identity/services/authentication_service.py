from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
import hashlib
import secrets

from domain.identity.entities import (
    AuthenticationAttempt,
    AuthenticationSession,
    PasswordResetRequest,
    RefreshSession,
)
from domain.identity.events import LoginFailed
from domain.identity.exceptions import IdentityDomainException
from domain.identity.policies import LoginAttemptPolicy
from domain.identity.repositories import (
    IAuthenticationAttemptRepository,
    IAuthenticationSessionRepository,
    IPasswordResetRequestRepository,
    IRefreshSessionRepository,
    IUserRepository,
)
from domain.identity.services.password_service import PasswordService
from domain.identity.value_objects import Email, Username


@dataclass(frozen=True, slots=True)
class AuthenticationTokens:
    """Opaque tokens returned after successful authentication."""

    access_token: str
    refresh_token: str
    session: AuthenticationSession
    refresh_session: RefreshSession


class AuthenticationService:
    """Domain service responsible for authentication workflows."""

    def __init__(
        self,
        users: IUserRepository,
        sessions: IAuthenticationSessionRepository,
        refresh_sessions: IRefreshSessionRepository,
        password_resets: IPasswordResetRequestRepository,
        attempts: IAuthenticationAttemptRepository,
        password_service: PasswordService,
        login_attempt_policy: LoginAttemptPolicy | None = None,
        session_duration: timedelta = timedelta(hours=8),
        refresh_duration: timedelta = timedelta(days=7),
        password_reset_duration: timedelta = timedelta(minutes=30),
    ) -> None:
        self._users = users
        self._sessions = sessions
        self._refresh_sessions = refresh_sessions
        self._password_resets = password_resets
        self._attempts = attempts
        self._password_service = password_service
        self._login_attempt_policy = login_attempt_policy or LoginAttemptPolicy()
        self._session_duration = session_duration
        self._refresh_duration = refresh_duration
        self._password_reset_duration = password_reset_duration

    def authenticate(self, username: Username, password: str) -> AuthenticationTokens:
        """Authenticate a user and create access and refresh sessions."""
        user = self._users.get_by_username(username)
        if user is None:
            self._record_attempt(username, False, "USER_NOT_FOUND")
            raise IdentityDomainException("Invalid credentials.")

        if not user.active:
            self._record_attempt(username, False, "USER_INACTIVE")
            user.add_domain_event(LoginFailed(username, "USER_INACTIVE"))
            raise IdentityDomainException("User is inactive.")

        if not self._login_attempt_policy.can_attempt_login(user):
            self._record_attempt(username, False, "USER_LOCKED")
            user.add_domain_event(LoginFailed(username, "USER_LOCKED"))
            raise IdentityDomainException("User is temporarily locked.")

        if not self._password_service.verify(password, user.password_hash):
            self._login_attempt_policy.register_failure(user)
            self._users.update(user)
            self._record_attempt(username, False, "INVALID_PASSWORD")
            user.add_domain_event(LoginFailed(username, "INVALID_PASSWORD"))
            raise IdentityDomainException("Invalid credentials.")

        self._login_attempt_policy.register_success(user)
        self._users.update(user)
        self._record_attempt(username, True, "AUTHENTICATED")
        return self._create_tokens(user.id)

    def logout(self, access_token: str) -> None:
        """Revoke an authentication session."""
        session = self._sessions.get_by_token_hash(self.hash_token(access_token))
        if session is None:
            return

        session.revoke()
        self._sessions.update(session)

    def validate_session(self, access_token: str) -> AuthenticationSession | None:
        """Return a valid session for an access token."""
        session = self._sessions.get_by_token_hash(self.hash_token(access_token))
        if session is None:
            return None

        if session.active:
            return session

        if session.status.value == "ACTIVE":
            session.expire()
            self._sessions.update(session)
        return None

    def renew_session(self, refresh_token: str) -> AuthenticationTokens:
        """Renew an access session using an active refresh token."""
        refresh_session = self._refresh_sessions.get_by_token_hash(self.hash_token(refresh_token))
        if refresh_session is None or not refresh_session.active:
            raise IdentityDomainException("Refresh session is invalid or expired.")

        current_session = self._sessions.get_by_id(refresh_session.session_id)
        if current_session is not None:
            current_session.revoke()
            self._sessions.update(current_session)

        refresh_session.revoke()
        self._refresh_sessions.update(refresh_session)
        return self._create_tokens(refresh_session.user_id)

    def request_password_reset(self, email: Email) -> tuple[str, PasswordResetRequest]:
        """Create a password reset request and return the raw token once."""
        user = self._users.get_by_email(email)
        if user is None:
            raise IdentityDomainException("User was not found.")

        token = self.new_token()
        reset_request = PasswordResetRequest.create(
            user.id,
            self.hash_token(token),
            datetime.now(UTC) + self._password_reset_duration,
        )
        self._password_resets.add(reset_request)
        return token, reset_request

    def confirm_password_reset(self, reset_token: str, new_password: str) -> None:
        """Change a password using an active reset token."""
        reset_request = self._password_resets.get_by_token_hash(self.hash_token(reset_token))
        if reset_request is None or not reset_request.active:
            raise IdentityDomainException("Password reset request is invalid or expired.")

        user = self._users.get_by_id(reset_request.user_id)
        if user is None:
            raise IdentityDomainException("User was not found.")

        user.change_password(self._password_service.hash_password(new_password))
        reset_request.mark_used()
        self._users.update(user)
        self._password_resets.update(reset_request)

    def change_password(self, username: Username, current_password: str, new_password: str) -> None:
        """Change a password after validating the current password."""
        user = self._users.get_by_username(username)
        if user is None or not self._password_service.verify(current_password, user.password_hash):
            raise IdentityDomainException("Invalid credentials.")

        user.change_password(self._password_service.hash_password(new_password))
        self._users.update(user)

    def _create_tokens(self, user_id: object) -> AuthenticationTokens:
        from shared.kernel.identity import Identity

        if not isinstance(user_id, Identity):
            raise IdentityDomainException("Invalid user identity.")

        access_token = self.new_token()
        refresh_token = self.new_token()
        session = AuthenticationSession.create(
            user_id,
            self.hash_token(access_token),
            datetime.now(UTC) + self._session_duration,
        )
        refresh_session = RefreshSession.create(
            user_id,
            session.id,
            self.hash_token(refresh_token),
            datetime.now(UTC) + self._refresh_duration,
        )
        self._sessions.add(session)
        self._refresh_sessions.add(refresh_session)
        return AuthenticationTokens(access_token, refresh_token, session, refresh_session)

    def _record_attempt(self, username: Username, successful: bool, reason: str) -> None:
        self._attempts.add(AuthenticationAttempt.record(username, successful, reason))

    @staticmethod
    def new_token() -> str:
        """Create a secure opaque token."""
        return secrets.token_urlsafe(48)

    @staticmethod
    def hash_token(token: str) -> str:
        """Hash an opaque token for persistence and lookup."""
        return hashlib.sha256(token.encode("utf-8")).hexdigest()

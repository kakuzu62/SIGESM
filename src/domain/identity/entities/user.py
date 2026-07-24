from __future__ import annotations

from datetime import UTC, datetime

from domain.identity.entities.role import Role
from domain.identity.events import PasswordChanged, UserActivated, UserCreated, UserDeactivated
from domain.identity.exceptions import IdentityDomainException
from domain.identity.value_objects import Email, PasswordHash, Username
from shared.kernel.aggregate_root import AggregateRoot
from shared.kernel.identity import Identity


class User(AggregateRoot[Identity]):
    """Aggregate root representing an application user."""

    __slots__ = (
        "_full_name",
        "_username",
        "_email",
        "_password_hash",
        "_roles",
        "_active",
        "_failed_login_attempts",
        "_locked_until",
        "_created_at",
        "_updated_at",
    )

    def __init__(
        self,
        entity_id: Identity,
        full_name: str,
        username: Username,
        email: Email,
        password_hash: PasswordHash,
        roles: tuple[Role, ...],
        active: bool,
        failed_login_attempts: int,
        locked_until: datetime | None,
        created_at: datetime,
        updated_at: datetime,
    ) -> None:
        super().__init__(entity_id)
        self._full_name = self._normalize_full_name(full_name)
        self._username = username
        self._email = email
        self._password_hash = password_hash
        self._roles = roles
        self._active = active
        self._failed_login_attempts = failed_login_attempts
        self._locked_until = locked_until
        self._created_at = created_at
        self._updated_at = updated_at

    @classmethod
    def create(
        cls,
        username: Username,
        email: Email,
        password_hash: PasswordHash,
        full_name: str | None = None,
    ) -> User:
        """Create an active user and record a domain event."""
        now = datetime.now(UTC)
        user = cls(
            entity_id=Identity.new(),
            full_name=full_name or username.value,
            username=username,
            email=email,
            password_hash=password_hash,
            roles=(),
            active=True,
            failed_login_attempts=0,
            locked_until=None,
            created_at=now,
            updated_at=now,
        )
        user.add_domain_event(UserCreated(user.id, username, email))
        return user

    @property
    def full_name(self) -> str:
        """Return the user's full name."""
        return self._full_name

    @property
    def username(self) -> Username:
        """Return username."""
        return self._username

    @property
    def email(self) -> Email:
        """Return email address."""
        return self._email

    @property
    def password_hash(self) -> PasswordHash:
        """Return encoded password hash."""
        return self._password_hash

    @property
    def roles(self) -> tuple[Role, ...]:
        """Return assigned roles."""
        return self._roles

    @property
    def active(self) -> bool:
        """Return whether user is active."""
        return self._active

    @property
    def failed_login_attempts(self) -> int:
        """Return failed login attempt count."""
        return self._failed_login_attempts

    @property
    def locked_until(self) -> datetime | None:
        """Return lock expiration timestamp when locked."""
        return self._locked_until

    @property
    def created_at(self) -> datetime:
        """Return creation timestamp."""
        return self._created_at

    @property
    def updated_at(self) -> datetime:
        """Return update timestamp."""
        return self._updated_at

    def assign_role(self, role: Role) -> None:
        """Assign a role to the user."""
        if role in self._roles:
            return

        self._roles = (*self._roles, role)
        self._touch()

    def remove_role(self, role: Role) -> None:
        """Remove a role from the user."""
        self._roles = tuple(item for item in self._roles if item != role)
        self._touch()

    def update_profile(self, full_name: str, username: Username, email: Email) -> None:
        """Update editable profile fields while preserving identity and credentials."""
        normalized_full_name = self._normalize_full_name(full_name)
        if (
            self._full_name == normalized_full_name
            and self._username == username
            and self._email == email
        ):
            return

        self._full_name = normalized_full_name
        self._username = username
        self._email = email
        self._touch()

    def activate(self, occurred_at: datetime | None = None) -> None:
        """Activate the user."""
        if self._active:
            return

        self._active = True
        self._touch(occurred_at)
        self.add_domain_event(UserActivated(self.id))

    def deactivate(self, reason: str, occurred_at: datetime | None = None) -> None:
        """Deactivate the user with an auditable reason."""
        if not reason.strip():
            raise IdentityDomainException("Deactivation reason is required.")

        if not self._active:
            return

        self._active = False
        self._touch(occurred_at)
        self.add_domain_event(UserDeactivated(self.id, reason.strip()))

    def change_password(self, password_hash: PasswordHash) -> None:
        """Change user password hash."""
        self._password_hash = password_hash
        self._touch()
        self.add_domain_event(PasswordChanged(self.id))

    def register_failed_login(self) -> None:
        """Increment failed login attempts."""
        self._failed_login_attempts += 1
        self._touch()

    def clear_failed_logins(self) -> None:
        """Clear failed login attempts."""
        self._failed_login_attempts = 0
        self._locked_until = None
        self._touch()

    def lock_until(self, locked_until: datetime) -> None:
        """Lock user authentication until the given timestamp."""
        self._locked_until = locked_until
        self._touch()

    def _touch(self, occurred_at: datetime | None = None) -> None:
        self._updated_at = occurred_at or datetime.now(UTC)

    @staticmethod
    def _normalize_full_name(full_name: str) -> str:
        normalized = " ".join(full_name.strip().split())
        if not normalized:
            raise IdentityDomainException("Full name is required.")
        if len(normalized) > 120:
            raise IdentityDomainException("Full name must contain at most 120 characters.")
        return normalized

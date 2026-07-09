from __future__ import annotations

from datetime import UTC, datetime, timedelta

from domain.identity.entities import User


class LoginAttemptPolicy:
    """Policy prepared to lock users after repeated authentication failures."""

    def __init__(self, max_attempts: int = 5, lock_minutes: int = 15) -> None:
        self._max_attempts = max_attempts
        self._lock_duration = timedelta(minutes=lock_minutes)

    @property
    def max_attempts(self) -> int:
        """Return configured maximum attempts before lock."""
        return self._max_attempts

    @property
    def lock_duration(self) -> timedelta:
        """Return configured lock duration."""
        return self._lock_duration

    def can_attempt_login(self, user: User) -> bool:
        """Return whether the user can attempt authentication."""
        if user.locked_until is None:
            return True

        return user.locked_until <= datetime.now(UTC)

    def register_failure(self, user: User) -> None:
        """Record a failed login and lock the user when the threshold is reached."""
        user.register_failed_login()
        if user.failed_login_attempts >= self._max_attempts:
            user.lock_until(datetime.now(UTC) + self._lock_duration)

    def register_success(self, user: User) -> None:
        """Clear failed attempts after a successful login."""
        user.clear_failed_logins()

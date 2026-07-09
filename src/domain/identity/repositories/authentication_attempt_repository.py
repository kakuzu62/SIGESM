from __future__ import annotations

from domain.contracts.repository import IRepository
from domain.identity.entities import AuthenticationAttempt
from shared.kernel.identity import Identity


class IAuthenticationAttemptRepository(IRepository[AuthenticationAttempt, Identity]):
    """Repository contract for authentication attempt audit records."""

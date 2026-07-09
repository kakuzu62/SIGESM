from __future__ import annotations

from collections.abc import Sequence

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from domain.identity.entities import AuthenticationAttempt
from domain.identity.repositories import IAuthenticationAttemptRepository
from infrastructure.persistence.sqlalchemy.identity.mappers import IdentityMapper
from infrastructure.persistence.sqlalchemy.identity.models import AuthenticationAttemptModel
from shared.kernel.identity import Identity


class SqlAlchemyAuthenticationAttemptRepository(IAuthenticationAttemptRepository):
    """SQLAlchemy repository for authentication attempts."""

    def __init__(self, session: Session) -> None:
        self._session = session

    def add(self, entity: AuthenticationAttempt) -> AuthenticationAttempt:
        """Add an authentication attempt."""
        self._session.merge(IdentityMapper.authentication_attempt_to_model(entity))
        return entity

    def update(self, entity: AuthenticationAttempt) -> AuthenticationAttempt:
        """Update an authentication attempt."""
        self._session.merge(IdentityMapper.authentication_attempt_to_model(entity))
        return entity

    def delete(self, entity: AuthenticationAttempt) -> None:
        """Delete an authentication attempt."""
        model = self._session.get(AuthenticationAttemptModel, str(entity.id))
        if model is not None:
            self._session.delete(model)

    def get_by_id(self, entity_id: Identity) -> AuthenticationAttempt | None:
        """Return an authentication attempt by identity."""
        model = self._session.get(AuthenticationAttemptModel, str(entity_id))
        if model is None:
            return None
        return IdentityMapper.authentication_attempt_to_domain(model)

    def exists(self, entity_id: Identity) -> bool:
        """Return whether an authentication attempt exists."""
        return self._session.get(AuthenticationAttemptModel, str(entity_id)) is not None

    def count(self) -> int:
        """Return authentication attempt count."""
        return self._session.execute(
            select(func.count()).select_from(AuthenticationAttemptModel)
        ).scalar_one()

    def list(self) -> Sequence[AuthenticationAttempt]:
        """Return authentication attempts."""
        return tuple(
            IdentityMapper.authentication_attempt_to_domain(model)
            for model in self._session.scalars(select(AuthenticationAttemptModel)).all()
        )

    def first(self) -> AuthenticationAttempt | None:
        """Return first authentication attempt."""
        model = self._session.scalars(select(AuthenticationAttemptModel).limit(1)).first()
        if model is None:
            return None
        return IdentityMapper.authentication_attempt_to_domain(model)

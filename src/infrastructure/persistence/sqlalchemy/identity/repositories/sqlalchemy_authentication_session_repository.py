from __future__ import annotations

from collections.abc import Sequence

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from domain.identity.entities import AuthenticationSession
from domain.identity.repositories import IAuthenticationSessionRepository
from infrastructure.persistence.sqlalchemy.identity.mappers import IdentityMapper
from infrastructure.persistence.sqlalchemy.identity.models import AuthenticationSessionModel
from shared.kernel.identity import Identity


class SqlAlchemyAuthenticationSessionRepository(IAuthenticationSessionRepository):
    """SQLAlchemy repository for authentication sessions."""

    def __init__(self, session: Session) -> None:
        self._session = session

    def add(self, entity: AuthenticationSession) -> AuthenticationSession:
        """Add an authentication session."""
        self._session.merge(IdentityMapper.authentication_session_to_model(entity))
        return entity

    def update(self, entity: AuthenticationSession) -> AuthenticationSession:
        """Update an authentication session."""
        self._session.merge(IdentityMapper.authentication_session_to_model(entity))
        return entity

    def delete(self, entity: AuthenticationSession) -> None:
        """Delete an authentication session."""
        model = self._session.get(AuthenticationSessionModel, str(entity.id))
        if model is not None:
            self._session.delete(model)

    def get_by_id(self, entity_id: Identity) -> AuthenticationSession | None:
        """Return an authentication session by identity."""
        model = self._session.get(AuthenticationSessionModel, str(entity_id))
        if model is None:
            return None
        return IdentityMapper.authentication_session_to_domain(model)

    def get_by_token_hash(self, token_hash: str) -> AuthenticationSession | None:
        """Return an authentication session by token hash."""
        model = self._session.scalars(
            select(AuthenticationSessionModel).where(
                AuthenticationSessionModel.token_hash == token_hash
            )
        ).one_or_none()
        if model is None:
            return None
        return IdentityMapper.authentication_session_to_domain(model)

    def list_active_by_user(self, user_id: Identity) -> tuple[AuthenticationSession, ...]:
        """Return active sessions for a user."""
        models = self._session.scalars(
            select(AuthenticationSessionModel).where(
                AuthenticationSessionModel.user_id == str(user_id),
                AuthenticationSessionModel.status == "ACTIVE",
            )
        ).all()
        return tuple(IdentityMapper.authentication_session_to_domain(model) for model in models)

    def exists(self, entity_id: Identity) -> bool:
        """Return whether an authentication session exists."""
        return self._session.get(AuthenticationSessionModel, str(entity_id)) is not None

    def count(self) -> int:
        """Return authentication session count."""
        return self._session.execute(
            select(func.count()).select_from(AuthenticationSessionModel)
        ).scalar_one()

    def list(self) -> Sequence[AuthenticationSession]:
        """Return authentication sessions."""
        return tuple(
            IdentityMapper.authentication_session_to_domain(model)
            for model in self._session.scalars(select(AuthenticationSessionModel)).all()
        )

    def first(self) -> AuthenticationSession | None:
        """Return first authentication session."""
        model = self._session.scalars(select(AuthenticationSessionModel).limit(1)).first()
        if model is None:
            return None
        return IdentityMapper.authentication_session_to_domain(model)

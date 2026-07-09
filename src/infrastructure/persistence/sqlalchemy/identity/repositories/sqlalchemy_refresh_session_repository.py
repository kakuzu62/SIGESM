from __future__ import annotations

from collections.abc import Sequence

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from domain.identity.entities import RefreshSession
from domain.identity.repositories import IRefreshSessionRepository
from infrastructure.persistence.sqlalchemy.identity.mappers import IdentityMapper
from infrastructure.persistence.sqlalchemy.identity.models import RefreshSessionModel
from shared.kernel.identity import Identity


class SqlAlchemyRefreshSessionRepository(IRefreshSessionRepository):
    """SQLAlchemy repository for refresh sessions."""

    def __init__(self, session: Session) -> None:
        self._session = session

    def add(self, entity: RefreshSession) -> RefreshSession:
        """Add a refresh session."""
        self._session.merge(IdentityMapper.refresh_session_to_model(entity))
        return entity

    def update(self, entity: RefreshSession) -> RefreshSession:
        """Update a refresh session."""
        self._session.merge(IdentityMapper.refresh_session_to_model(entity))
        return entity

    def delete(self, entity: RefreshSession) -> None:
        """Delete a refresh session."""
        model = self._session.get(RefreshSessionModel, str(entity.id))
        if model is not None:
            self._session.delete(model)

    def get_by_id(self, entity_id: Identity) -> RefreshSession | None:
        """Return a refresh session by identity."""
        model = self._session.get(RefreshSessionModel, str(entity_id))
        if model is None:
            return None
        return IdentityMapper.refresh_session_to_domain(model)

    def get_by_token_hash(self, token_hash: str) -> RefreshSession | None:
        """Return a refresh session by token hash."""
        model = self._session.scalars(
            select(RefreshSessionModel).where(RefreshSessionModel.token_hash == token_hash)
        ).one_or_none()
        if model is None:
            return None
        return IdentityMapper.refresh_session_to_domain(model)

    def exists(self, entity_id: Identity) -> bool:
        """Return whether a refresh session exists."""
        return self._session.get(RefreshSessionModel, str(entity_id)) is not None

    def count(self) -> int:
        """Return refresh session count."""
        return self._session.execute(
            select(func.count()).select_from(RefreshSessionModel)
        ).scalar_one()

    def list(self) -> Sequence[RefreshSession]:
        """Return refresh sessions."""
        return tuple(
            IdentityMapper.refresh_session_to_domain(model)
            for model in self._session.scalars(select(RefreshSessionModel)).all()
        )

    def first(self) -> RefreshSession | None:
        """Return first refresh session."""
        model = self._session.scalars(select(RefreshSessionModel).limit(1)).first()
        if model is None:
            return None
        return IdentityMapper.refresh_session_to_domain(model)

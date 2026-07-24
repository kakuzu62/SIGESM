from __future__ import annotations

from collections.abc import Iterator
from pathlib import Path
from types import TracebackType

import pytest
from PySide6.QtWidgets import QApplication

from core.config.settings import DatabaseSettings
from core.database.base import Base
from core.database.engine import DatabaseEngineFactory
from core.database.session import DatabaseSessionFactory
from domain.identity.entities import User
from domain.identity.policies import LoginAttemptPolicy
from domain.identity.repositories import (
    IUserRepository,
)
from domain.identity.services import AuthenticationService, PasswordService
from domain.identity.value_objects import Email, PasswordHash, Username
from infrastructure.identity import (
    InMemoryAuthenticationAttemptRepository,
    InMemoryAuthenticationSessionRepository,
    InMemoryPasswordResetRequestRepository,
    InMemoryRefreshSessionRepository,
    InMemoryUserRepository,
)
from infrastructure.persistence.sqlalchemy.identity.models import UserModel
from infrastructure.persistence.sqlalchemy.identity.repositories import SqlAlchemyUserRepository
from presentation.modules.user_management.application import (
    ChangeUserActiveStatusService,
    UserListingService,
)
from presentation.modules.user_management.application.commands.change_user_status import (
    ChangeUserActiveStatusCommand,
    ChangeUserActiveStatusHandler,
)
from presentation.modules.user_management.application.commands.change_user_status.unit_of_work import (
    UserStatusConflictError,
    UserStatusUnitOfWork,
    UserStatusUnitOfWorkFactory,
)
from presentation.modules.user_management.application.commands.change_user_status.validator import (
    ChangeUserActiveStatusCommandValidator,
)
from presentation.modules.user_management.application.queries.list_users import (
    ListUsersQuery,
    UserListItemDTO,
)
from presentation.modules.user_management.infrastructure.persistence import (
    SqlAlchemyUserStatusUnitOfWorkFactory,
)
from presentation.modules.user_management.infrastructure.repositories import (
    InMemoryUserListingRepository,
    InMemoryUserStatusUnitOfWorkFactory,
)
from presentation.modules.user_management.presentation.viewmodels import (
    ChangeUserActiveStatusViewModel,
)
from shared.kernel.identity import Identity

_VALID_ARGON2ID_HASH = (
    "$argon2id$v=19$m=65536,t=3,p=4$"
    "c2lnZXNtX3Rlc3Rfc2FsdA$"
    "F5agQp7LdbYQlwU++q7RrA3y8nY5jD9O81jHT2e66eE"
)


class _ConflictOnCommitUnitOfWork(UserStatusUnitOfWork):
    def __init__(self, users: IUserRepository) -> None:
        self._users = users
        self.rollbacks = 0

    @property
    def users(self) -> IUserRepository:
        return self._users

    def __enter__(self) -> _ConflictOnCommitUnitOfWork:
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        if exc_type is not None:
            self.rollback()

    def commit(self) -> None:
        raise UserStatusConflictError("conflict")

    def rollback(self) -> None:
        self.rollbacks += 1


class _ConflictOnCommitFactory(UserStatusUnitOfWorkFactory):
    def __init__(self, users: IUserRepository) -> None:
        self.unit_of_work = _ConflictOnCommitUnitOfWork(users)

    def create(self) -> _ConflictOnCommitUnitOfWork:
        return self.unit_of_work


@pytest.fixture
def qt_app() -> QApplication:
    """Return a QApplication for signal-based tests."""
    application = QApplication.instance()
    if isinstance(application, QApplication):
        return application
    return QApplication([])


@pytest.fixture
def identity_session_factory(tmp_path: Path) -> Iterator[DatabaseSessionFactory]:
    """Create an isolated identity database."""
    database_settings = DatabaseSettings(database=str(tmp_path / "identity_status.db"))
    factory = DatabaseSessionFactory.from_engine_factory(DatabaseEngineFactory(database_settings))
    _ = UserModel
    Base.metadata.create_all(factory.engine)
    yield factory
    Base.metadata.drop_all(factory.engine)


def test_user_activate_and_deactivate_preserve_protected_fields() -> None:
    user = _user("manager", "manager@sigesm.local", "Manager User")
    original_id = user.id
    original_hash = user.password_hash
    original_full_name = user.full_name
    original_username = user.username
    original_email = user.email
    original_roles = user.roles
    original_created_at = user.created_at
    original_updated_at = user.updated_at

    user.deactivate("Administrative deactivation.")

    assert not user.active
    assert user.updated_at >= original_updated_at
    assert user.id == original_id
    assert user.password_hash == original_hash
    assert user.full_name == original_full_name
    assert user.username == original_username
    assert user.email == original_email
    assert user.roles == original_roles
    assert user.created_at == original_created_at

    deactivated_at = user.updated_at
    user.activate()

    assert user.active
    assert user.updated_at >= deactivated_at
    assert user.id == original_id
    assert user.password_hash == original_hash


def test_user_same_state_is_idempotent_in_domain() -> None:
    user = _user("manager", "manager@sigesm.local", "Manager User")
    updated_at = user.updated_at

    user.activate()

    assert user.active
    assert user.updated_at == updated_at


def test_status_validator_rejects_invalid_identifiers() -> None:
    validator = ChangeUserActiveStatusCommandValidator()
    user_id = str(Identity.new())

    assert validator.validate(ChangeUserActiveStatusCommand("", user_id, True)).is_failure
    assert validator.validate(ChangeUserActiveStatusCommand(user_id, "", True)).is_failure
    assert validator.validate(ChangeUserActiveStatusCommand("invalid", user_id, True)).is_failure


def test_status_handler_deactivates_and_commits() -> None:
    users = InMemoryUserRepository()
    actor = _user("actor", "actor@sigesm.local", "Actor User")
    target = _user("target", "target@sigesm.local", "Target User")
    users.add(actor)
    users.add(target)
    factory = InMemoryUserStatusUnitOfWorkFactory(users)

    result = ChangeUserActiveStatusHandler(factory).handle(
        ChangeUserActiveStatusCommand(str(actor.id), str(target.id), False)
    )

    assert result.is_success
    assert not result.value.active
    assert not hasattr(result.value, "password")
    assert not hasattr(result.value, "password_hash")
    assert factory.created[0].commits == 1
    assert factory.created[0].rollbacks == 0
    persisted = users.get_by_id(target.id)
    assert persisted is not None
    assert not persisted.active


def test_status_handler_activates_inactive_user() -> None:
    users = InMemoryUserRepository()
    actor = _user("actor", "actor@sigesm.local", "Actor User")
    target = _user("target", "target@sigesm.local", "Target User")
    target.deactivate("Administrative deactivation.")
    users.add(actor)
    users.add(target)

    result = ChangeUserActiveStatusHandler(InMemoryUserStatusUnitOfWorkFactory(users)).handle(
        ChangeUserActiveStatusCommand(str(actor.id), str(target.id), True)
    )

    assert result.is_success
    assert result.value.active


def test_status_handler_rejects_missing_user_self_deactivation_and_same_state() -> None:
    users = InMemoryUserRepository()
    actor = _user("actor", "actor@sigesm.local", "Actor User")
    users.add(actor)
    factory = InMemoryUserStatusUnitOfWorkFactory(users)

    missing = ChangeUserActiveStatusHandler(factory).handle(
        ChangeUserActiveStatusCommand(str(actor.id), str(Identity.new()), False)
    )
    self_deactivation = ChangeUserActiveStatusHandler(factory).handle(
        ChangeUserActiveStatusCommand(str(actor.id), str(actor.id), False)
    )
    same_state = ChangeUserActiveStatusHandler(factory).handle(
        ChangeUserActiveStatusCommand(str(actor.id), str(actor.id), True)
    )

    assert missing.is_failure
    assert missing.error == "Usuario nao encontrado."
    assert self_deactivation.is_failure
    assert self_deactivation.error == "Voce nao pode desativar a propria conta."
    assert same_state.is_failure
    assert same_state.error == "Usuario ja esta ativo."
    assert factory.created[0].rollbacks == 1
    assert factory.created[1].rollbacks == 1
    assert factory.created[2].rollbacks == 1


def test_status_handler_allows_self_activation_consistently() -> None:
    users = InMemoryUserRepository()
    actor = _user("actor", "actor@sigesm.local", "Actor User")
    actor.deactivate("Administrative deactivation.")
    users.add(actor)

    result = ChangeUserActiveStatusHandler(InMemoryUserStatusUnitOfWorkFactory(users)).handle(
        ChangeUserActiveStatusCommand(str(actor.id), str(actor.id), True)
    )

    assert result.is_success
    assert result.value.active


def test_status_handler_rolls_back_commit_conflict() -> None:
    users = InMemoryUserRepository()
    actor = _user("actor", "actor@sigesm.local", "Actor User")
    target = _user("target", "target@sigesm.local", "Target User")
    users.add(actor)
    users.add(target)
    factory = _ConflictOnCommitFactory(users)

    result = ChangeUserActiveStatusHandler(factory).handle(
        ChangeUserActiveStatusCommand(str(actor.id), str(target.id), False)
    )

    assert result.is_failure
    assert result.error == "Nao foi possivel alterar o status do usuario."
    assert factory.unit_of_work.rollbacks == 1


def test_status_view_model_requests_confirmation_and_changes_status(
    qt_app: QApplication,
) -> None:
    users = InMemoryUserRepository()
    actor = _user("actor", "actor@sigesm.local", "Actor User")
    target = _user("target", "target@sigesm.local", "Target User")
    users.add(actor)
    users.add(target)
    view_model = ChangeUserActiveStatusViewModel(
        str(actor.id),
        ChangeUserActiveStatusService(InMemoryUserStatusUnitOfWorkFactory(users)),
    )
    item = _listing_item(users, target.id)
    confirmations: list[str] = []
    changed: list[object] = []
    failed: list[str] = []
    view_model.confirmation_requested.connect(confirmations.append)
    view_model.status_changed.connect(lambda updated: changed.append(updated))
    view_model.status_change_failed.connect(failed.append)

    view_model.request_change_status(item)

    assert len(confirmations) == 1
    assert "desativar" in confirmations[0]
    assert view_model.can_change_status

    view_model.confirm_change_status()

    assert len(changed) == 1
    assert failed == []
    assert not view_model.is_loading
    persisted = users.get_by_id(target.id)
    assert persisted is not None
    assert not persisted.active
    qt_app.processEvents()


def test_status_view_model_cancel_and_empty_selection_do_not_call_service(
    qt_app: QApplication,
) -> None:
    users = InMemoryUserRepository()
    actor = _user("actor", "actor@sigesm.local", "Actor User")
    users.add(actor)
    factory = InMemoryUserStatusUnitOfWorkFactory(users)
    view_model = ChangeUserActiveStatusViewModel(
        str(actor.id), ChangeUserActiveStatusService(factory)
    )
    confirmations: list[str] = []
    view_model.confirmation_requested.connect(confirmations.append)

    view_model.request_change_status(None)
    view_model.cancel_change_status()
    view_model.confirm_change_status()

    assert confirmations == []
    assert factory.created == []
    qt_app.processEvents()


def test_status_view_model_reports_failure_and_uses_actor_id(
    qt_app: QApplication,
) -> None:
    users = InMemoryUserRepository()
    actor = _user("actor", "actor@sigesm.local", "Actor User")
    users.add(actor)
    view_model = ChangeUserActiveStatusViewModel(
        str(actor.id),
        ChangeUserActiveStatusService(InMemoryUserStatusUnitOfWorkFactory(users)),
    )
    item = _listing_item(users, actor.id)
    failures: list[str] = []
    view_model.status_change_failed.connect(failures.append)

    view_model.request_change_status(item)
    view_model.confirm_change_status()

    assert failures == ["Voce nao pode desativar a propria conta."]
    assert view_model.general_error == "Voce nao pode desativar a propria conta."
    assert actor.active
    qt_app.processEvents()


def test_sqlalchemy_user_status_persists_and_listing_reflects_change(
    identity_session_factory: DatabaseSessionFactory,
) -> None:
    with identity_session_factory.context() as session:
        repository = SqlAlchemyUserRepository(session)
        actor = _user("actor", "actor@sigesm.local", "Actor User")
        target = _user("target", "target@sigesm.local", "Target User")
        repository.add(actor)
        repository.add(target)
        session.commit()
        actor_id = str(actor.id)
        target_id = str(target.id)

    result = ChangeUserActiveStatusService(
        SqlAlchemyUserStatusUnitOfWorkFactory(identity_session_factory)
    ).change_status(ChangeUserActiveStatusCommand(actor_id, target_id, False))

    assert result.is_success
    with identity_session_factory.context() as session:
        repository = SqlAlchemyUserRepository(session)
        persisted = repository.get_by_id(Identity.from_string(target_id))
        assert persisted is not None
        assert not persisted.active
        listed = UserListingService(InMemoryUserListingRepository(repository)).list_users(
            ListUsersQuery()
        )
        assert listed.is_success
        status = {item.id: item.status for item in listed.value.items}
        assert status[target_id] == "Inativo"


def test_sqlalchemy_status_rollback_preserves_state(
    identity_session_factory: DatabaseSessionFactory,
) -> None:
    with identity_session_factory.context() as session:
        repository = SqlAlchemyUserRepository(session)
        user = _user("actor", "actor@sigesm.local", "Actor User")
        repository.add(user)
        session.commit()
        user_id = str(user.id)

    result = ChangeUserActiveStatusService(
        SqlAlchemyUserStatusUnitOfWorkFactory(identity_session_factory)
    ).change_status(ChangeUserActiveStatusCommand(user_id, user_id, False))

    assert result.is_failure
    with identity_session_factory.context() as session:
        repository = SqlAlchemyUserRepository(session)
        persisted = repository.get_by_id(Identity.from_string(user_id))
        assert persisted is not None
        assert persisted.active


def test_authentication_rejects_inactive_user_with_safe_message() -> None:
    users = InMemoryUserRepository()
    password_service = PasswordService()
    active = User.create(
        Username("active"),
        Email("active@sigesm.local"),
        password_service.hash_password("Strong#123"),
        full_name="Active User",
    )
    inactive = User.create(
        Username("inactive"),
        Email("inactive@sigesm.local"),
        password_service.hash_password("Strong#123"),
        full_name="Inactive User",
    )
    inactive.deactivate("Administrative deactivation.")
    users.add(active)
    users.add(inactive)
    authentication = _authentication_service(users)

    tokens = authentication.authenticate(Username("active"), "Strong#123")

    assert str(tokens.session.user_id) == str(active.id)
    with pytest.raises(Exception, match="inactive"):
        authentication.authenticate(Username("inactive"), "Strong#123")
    with pytest.raises(Exception):
        authentication.authenticate(Username("active"), "Wrong#123")
    with pytest.raises(Exception):
        authentication.authenticate(Username("missing"), "Strong#123")


def _authentication_service(users: IUserRepository) -> AuthenticationService:
    return AuthenticationService(
        users=users,
        sessions=InMemoryAuthenticationSessionRepository(),
        refresh_sessions=InMemoryRefreshSessionRepository(),
        password_resets=InMemoryPasswordResetRequestRepository(),
        attempts=InMemoryAuthenticationAttemptRepository(),
        password_service=PasswordService(),
        login_attempt_policy=LoginAttemptPolicy(max_attempts=5, lock_minutes=15),
    )


def _user(username: str, email: str, full_name: str) -> User:
    return User.create(
        Username(username),
        Email(email),
        PasswordHash(_VALID_ARGON2ID_HASH),
        full_name=full_name,
    )


def _listing_item(users: IUserRepository, user_id: Identity) -> UserListItemDTO:
    result = UserListingService(InMemoryUserListingRepository(users)).list_users(ListUsersQuery())
    assert result.is_success
    return next(item for item in result.value.items if item.id == str(user_id))

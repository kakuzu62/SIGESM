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
from domain.identity.repositories import IUserRepository
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
    ResetPasswordService,
    UserListingService,
)
from presentation.modules.user_management.application.commands.reset_password import (
    ResetPasswordCommand,
    ResetPasswordHandler,
)
from presentation.modules.user_management.application.commands.reset_password.unit_of_work import (
    PasswordResetPersistenceError,
    ResetPasswordUnitOfWork,
    ResetPasswordUnitOfWorkFactory,
)
from presentation.modules.user_management.application.commands.reset_password.validator import (
    ResetPasswordCommandValidator,
)
from presentation.modules.user_management.application.queries.list_users import (
    ListUsersQuery,
    UserListItemDTO,
)
from presentation.modules.user_management.infrastructure.persistence import (
    SqlAlchemyResetPasswordUnitOfWorkFactory,
)
from presentation.modules.user_management.infrastructure.repositories import (
    InMemoryResetPasswordUnitOfWorkFactory,
    InMemoryUserListingRepository,
)
from presentation.modules.user_management.presentation.dialogs import ResetPasswordDialog
from presentation.modules.user_management.presentation.viewmodels import ResetPasswordViewModel
from shared.kernel.identity import Identity

_VALID_ARGON2ID_HASH = (
    "$argon2id$v=19$m=65536,t=3,p=4$"
    "c2lnZXNtX3Rlc3Rfc2FsdA$"
    "F5agQp7LdbYQlwU++q7RrA3y8nY5jD9O81jHT2e66eE"
)
_NEW_HASH = (
    "$argon2id$v=19$m=65536,t=3,p=4$"
    "bmV3X3N1cGVyX3NhbHQ$"
    "Ls7q8mY1p1tEel13CuuFZd1nM1upB0Qp18h1mgDnr30"
)


class _RecordingPasswordService(PasswordService):
    def __init__(self) -> None:
        self.received_passwords: list[str] = []

    def hash_password(self, raw_password: str) -> PasswordHash:
        self.received_passwords.append(raw_password)
        return PasswordHash(_NEW_HASH)


class _ConflictOnCommitUnitOfWork(ResetPasswordUnitOfWork):
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
        raise PasswordResetPersistenceError("conflict")

    def rollback(self) -> None:
        self.rollbacks += 1


class _ConflictOnCommitFactory(ResetPasswordUnitOfWorkFactory):
    def __init__(self, users: IUserRepository) -> None:
        self.unit_of_work = _ConflictOnCommitUnitOfWork(users)

    def create(self) -> _ConflictOnCommitUnitOfWork:
        return self.unit_of_work


@pytest.fixture
def qt_app() -> QApplication:
    """Return a QApplication for widget tests."""
    application = QApplication.instance()
    if isinstance(application, QApplication):
        return application
    return QApplication([])


@pytest.fixture
def identity_session_factory(tmp_path: Path) -> Iterator[DatabaseSessionFactory]:
    """Create an isolated identity database."""
    database_settings = DatabaseSettings(database=str(tmp_path / "identity_password_reset.db"))
    factory = DatabaseSessionFactory.from_engine_factory(DatabaseEngineFactory(database_settings))
    _ = UserModel
    Base.metadata.create_all(factory.engine)
    yield factory
    Base.metadata.drop_all(factory.engine)


def test_user_change_password_preserves_non_credentials() -> None:
    user = _user("manager", "manager@sigesm.local", "Manager User")
    original_id = user.id
    original_full_name = user.full_name
    original_username = user.username
    original_email = user.email
    original_active = user.active
    original_roles = user.roles
    original_created_at = user.created_at
    original_updated_at = user.updated_at

    user.change_password(PasswordHash(_NEW_HASH))

    assert user.password_hash.value == _NEW_HASH
    assert user.updated_at >= original_updated_at
    assert user.id == original_id
    assert user.full_name == original_full_name
    assert user.username == original_username
    assert user.email == original_email
    assert user.active == original_active
    assert user.roles == original_roles
    assert user.created_at == original_created_at


def test_reset_password_validator_rejects_invalid_input() -> None:
    validator = ResetPasswordCommandValidator()
    user_id = str(Identity.new())

    assert validator.validate(ResetPasswordCommand("", user_id, "Strong#123")).is_failure
    assert validator.validate(ResetPasswordCommand(user_id, "", "Strong#123")).is_failure
    assert validator.validate(ResetPasswordCommand(user_id, user_id, "")).is_failure
    assert validator.validate(ResetPasswordCommand("invalid", user_id, "Strong#123")).is_failure


def test_reset_password_handler_updates_hash_and_commits() -> None:
    users = InMemoryUserRepository()
    actor = _user("actor", "actor@sigesm.local", "Actor User")
    target = _user("target", "target@sigesm.local", "Target User")
    users.add(actor)
    users.add(target)
    factory = InMemoryResetPasswordUnitOfWorkFactory(users)
    password_service = _RecordingPasswordService()

    result = ResetPasswordHandler(factory, password_service).handle(
        ResetPasswordCommand(str(actor.id), str(target.id), "NewStrong#123")
    )

    assert result.is_success
    assert result.value.username == "target"
    assert not hasattr(result.value, "password")
    assert not hasattr(result.value, "password_hash")
    assert password_service.received_passwords == ["NewStrong#123"]
    assert factory.created[0].commits == 1
    assert factory.created[0].rollbacks == 0
    persisted = users.get_by_id(target.id)
    assert persisted is not None
    assert persisted.password_hash.value == _NEW_HASH


def test_reset_password_handler_rejects_missing_user_and_rolls_back() -> None:
    users = InMemoryUserRepository()
    actor = _user("actor", "actor@sigesm.local", "Actor User")
    users.add(actor)
    factory = InMemoryResetPasswordUnitOfWorkFactory(users)

    result = ResetPasswordHandler(factory, _RecordingPasswordService()).handle(
        ResetPasswordCommand(str(actor.id), str(Identity.new()), "NewStrong#123")
    )

    assert result.is_failure
    assert result.error == "Usuario nao encontrado."
    assert factory.created[0].rollbacks == 1


def test_reset_password_handler_rolls_back_persistence_error() -> None:
    users = InMemoryUserRepository()
    actor = _user("actor", "actor@sigesm.local", "Actor User")
    target = _user("target", "target@sigesm.local", "Target User")
    users.add(actor)
    users.add(target)
    factory = _ConflictOnCommitFactory(users)

    result = ResetPasswordHandler(factory, _RecordingPasswordService()).handle(
        ResetPasswordCommand(str(actor.id), str(target.id), "NewStrong#123")
    )

    assert result.is_failure
    assert result.error == "Nao foi possivel redefinir a senha."
    assert factory.unit_of_work.rollbacks == 1


def test_reset_password_handler_uses_password_policy() -> None:
    users = InMemoryUserRepository()
    actor = _user("actor", "actor@sigesm.local", "Actor User")
    target = _user("target", "target@sigesm.local", "Target User")
    users.add(actor)
    users.add(target)
    factory = InMemoryResetPasswordUnitOfWorkFactory(users)

    result = ResetPasswordHandler(factory, PasswordService()).handle(
        ResetPasswordCommand(str(actor.id), str(target.id), "weak")
    )

    assert result.is_failure
    assert "Password" in result.error
    assert factory.created[0].rollbacks == 1


def test_reset_password_view_model_validates_confirmation_and_submits(
    qt_app: QApplication,
) -> None:
    users = InMemoryUserRepository()
    actor = _user("actor", "actor@sigesm.local", "Actor User")
    target = _user("target", "target@sigesm.local", "Target User")
    users.add(actor)
    users.add(target)
    view_model = ResetPasswordViewModel(
        str(actor.id),
        _listing_item(users, target.id),
        ResetPasswordService(
            InMemoryResetPasswordUnitOfWorkFactory(users),
            _RecordingPasswordService(),
        ),
    )
    emitted: list[object] = []
    view_model.password_reset.connect(lambda user: emitted.append(user))

    assert not view_model.can_submit
    view_model.update_input("new_password", "NewStrong#123")
    view_model.update_input("confirm_password", "Different#123")
    view_model.submit()

    assert view_model.field_errors["confirm_password"] == (
        "A confirmacao da senha nao corresponde."
    )
    assert emitted == []

    view_model.update_input("confirm_password", "NewStrong#123")
    view_model.submit()

    assert len(emitted) == 1
    assert view_model.success
    assert not view_model.can_submit
    assert not view_model.is_loading
    qt_app.processEvents()


def test_reset_password_view_model_blocks_double_submit_and_reports_failure(
    qt_app: QApplication,
) -> None:
    users = InMemoryUserRepository()
    actor = _user("actor", "actor@sigesm.local", "Actor User")
    target = _user("target", "target@sigesm.local", "Target User")
    users.add(actor)
    users.add(target)
    factory = InMemoryResetPasswordUnitOfWorkFactory(users)
    view_model = ResetPasswordViewModel(
        str(actor.id),
        _listing_item(users, target.id),
        ResetPasswordService(factory, PasswordService()),
    )
    failures: list[str] = []
    view_model.reset_failed.connect(failures.append)
    view_model.update_input("new_password", "weak")
    view_model.update_input("confirm_password", "weak")
    view_model._set_loading(True)

    view_model.submit()

    assert factory.created == []
    view_model._set_loading(False)
    view_model.submit()
    assert failures
    assert view_model.general_error
    qt_app.processEvents()


def test_reset_password_dialog_opens_cancels_and_hides_passwords(
    qt_app: QApplication,
) -> None:
    users = InMemoryUserRepository()
    actor = _user("actor", "actor@sigesm.local", "Actor User")
    target = _user("target", "target@sigesm.local", "Target User")
    users.add(actor)
    users.add(target)
    view_model = ResetPasswordViewModel(
        str(actor.id),
        _listing_item(users, target.id),
        ResetPasswordService(
            InMemoryResetPasswordUnitOfWorkFactory(users),
            _RecordingPasswordService(),
        ),
    )
    dialog = ResetPasswordDialog(view_model)

    assert dialog.windowTitle() == "Redefinir senha"
    assert dialog._new_password.echoMode() == dialog._new_password.EchoMode.Password
    assert dialog._confirm_password.echoMode() == dialog._confirm_password.EchoMode.Password
    assert not dialog._save_button.isEnabled()

    dialog._new_password.setText("NewStrong#123")
    dialog._confirm_password.setText("NewStrong#123")
    assert dialog._save_button.isEnabled()
    dialog.reject()

    assert dialog._new_password.text() == ""
    assert dialog._confirm_password.text() == ""
    qt_app.processEvents()


def test_sqlalchemy_password_reset_persists(
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

    result = ResetPasswordService(
        SqlAlchemyResetPasswordUnitOfWorkFactory(identity_session_factory),
        _RecordingPasswordService(),
    ).reset_password(ResetPasswordCommand(actor_id, target_id, "NewStrong#123"))

    assert result.is_success
    with identity_session_factory.context() as session:
        repository = SqlAlchemyUserRepository(session)
        persisted = repository.get_by_id(Identity.from_string(target_id))
        assert persisted is not None
        assert persisted.password_hash.value == _NEW_HASH


def test_password_reset_allows_login_with_new_password_and_rejects_old() -> None:
    users = InMemoryUserRepository()
    password_service = PasswordService()
    actor = User.create(
        Username("actor"),
        Email("actor@sigesm.local"),
        password_service.hash_password("Actor#123"),
        full_name="Actor User",
    )
    target = User.create(
        Username("target"),
        Email("target@sigesm.local"),
        password_service.hash_password("OldStrong#123"),
        full_name="Target User",
    )
    users.add(actor)
    users.add(target)
    service = ResetPasswordService(
        InMemoryResetPasswordUnitOfWorkFactory(users),
        password_service,
    )

    result = service.reset_password(
        ResetPasswordCommand(str(actor.id), str(target.id), "NewStrong#123")
    )

    assert result.is_success
    authentication = _authentication_service(users, password_service)
    with pytest.raises(Exception):
        authentication.authenticate(Username("target"), "OldStrong#123")
    tokens = authentication.authenticate(Username("target"), "NewStrong#123")
    assert str(tokens.session.user_id) == str(target.id)


def _authentication_service(
    users: IUserRepository,
    password_service: PasswordService,
) -> AuthenticationService:
    return AuthenticationService(
        users=users,
        sessions=InMemoryAuthenticationSessionRepository(),
        refresh_sessions=InMemoryRefreshSessionRepository(),
        password_resets=InMemoryPasswordResetRequestRepository(),
        attempts=InMemoryAuthenticationAttemptRepository(),
        password_service=password_service,
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

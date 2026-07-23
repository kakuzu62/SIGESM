from __future__ import annotations

from collections.abc import Iterator
from pathlib import Path
from types import TracebackType

import pytest
from PySide6.QtWidgets import QApplication
from sqlalchemy.exc import IntegrityError

from core.config.settings import DatabaseSettings
from core.database.base import Base
from core.database.engine import DatabaseEngineFactory
from core.database.session import DatabaseSessionFactory
from domain.identity.entities import User
from domain.identity.repositories import IUserRepository
from domain.identity.services import PasswordService
from domain.identity.value_objects import Email, PasswordHash, Username
from infrastructure.identity import InMemoryUserRepository
from infrastructure.persistence.sqlalchemy.identity.models import UserModel
from presentation.modules.user_management.application import CreateUserService, UserListingService
from presentation.modules.user_management.application.commands.create_user import (
    CreateUserCommand,
    CreateUserHandler,
)
from presentation.modules.user_management.application.commands.create_user.unit_of_work import (
    UserCreationConflictError,
    UserCreationUnitOfWork,
    UserCreationUnitOfWorkFactory,
)
from presentation.modules.user_management.application.commands.create_user.validator import (
    CreateUserCommandValidator,
)
from presentation.modules.user_management.application.queries.list_users import ListUsersQuery
from presentation.modules.user_management.infrastructure.persistence import (
    SqlAlchemyUserCreationUnitOfWorkFactory,
)
from presentation.modules.user_management.infrastructure.repositories import (
    InMemoryUserCreationUnitOfWorkFactory,
    InMemoryUserListingRepository,
)
from presentation.modules.user_management.presentation.dialogs import UserFormDialog
from presentation.modules.user_management.presentation.viewmodels import CreateUserViewModel

_VALID_ARGON2ID_HASH = (
    "$argon2id$v=19$m=65536,t=3,p=4$"
    "c2lnZXNtX3Rlc3Rfc2FsdA$"
    "F5agQp7LdbYQlwU++q7RrA3y8nY5jD9O81jHT2e66eE"
)


class _RecordingPasswordService(PasswordService):
    def __init__(self) -> None:
        self.received_passwords: list[str] = []

    def hash_password(self, raw_password: str) -> PasswordHash:
        self.received_passwords.append(raw_password)
        if raw_password == "weak":
            return PasswordService().hash_password(raw_password)
        return PasswordHash(_VALID_ARGON2ID_HASH)


class _ConflictOnCommitUnitOfWork(UserCreationUnitOfWork):
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
        raise UserCreationConflictError("conflict")

    def rollback(self) -> None:
        self.rollbacks += 1


class _ConflictOnCommitFactory(UserCreationUnitOfWorkFactory):
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
    database_settings = DatabaseSettings(database=str(tmp_path / "identity_creation.db"))
    factory = DatabaseSessionFactory.from_engine_factory(DatabaseEngineFactory(database_settings))
    _ = UserModel
    Base.metadata.create_all(factory.engine)
    yield factory
    Base.metadata.drop_all(factory.engine)


def test_user_creation_accepts_full_name_and_initial_state() -> None:
    user = User.create(
        Username("operator"),
        Email("operator@sigesm.local"),
        PasswordHash(_VALID_ARGON2ID_HASH),
        full_name="Operator User",
    )

    assert user.full_name == "Operator User"
    assert user.active
    assert user.roles == ()
    assert user.locked_until is None
    assert user.created_at == user.updated_at


def test_create_user_validator_rejects_required_fields_and_limits() -> None:
    validator = CreateUserCommandValidator()

    assert validator.validate(
        CreateUserCommand(" ", "user", "u@sigesm.local", "Strong#123")
    ).is_failure
    assert validator.validate(
        CreateUserCommand("User", " ", "u@sigesm.local", "Strong#123")
    ).is_failure
    assert validator.validate(CreateUserCommand("User", "user", " ", "Strong#123")).is_failure
    assert validator.validate(CreateUserCommand("User", "user", "u@sigesm.local", "")).is_failure
    assert validator.validate(
        CreateUserCommand("A" * 121, "user", "u@sigesm.local", "Strong#123")
    ).is_failure


def test_create_user_validator_normalizes_input() -> None:
    result = CreateUserCommandValidator().validate(
        CreateUserCommand(
            "  User   Name  ", "  Admin.User  ", "  ADMIN@SIGESM.LOCAL  ", "Strong#123"
        )
    )

    assert result.is_success
    assert result.value.full_name == "User Name"
    assert result.value.username == "Admin.User"
    assert result.value.email == "ADMIN@SIGESM.LOCAL"


def test_create_user_handler_creates_user_and_commits() -> None:
    users = InMemoryUserRepository()
    factory = InMemoryUserCreationUnitOfWorkFactory(users)
    password_service = _RecordingPasswordService()
    handler = CreateUserHandler(factory, password_service)

    result = handler.handle(
        CreateUserCommand("Manager User", "manager", "manager@sigesm.local", "Strong#123")
    )

    assert result.is_success
    assert result.value.full_name == "Manager User"
    assert result.value.username == "manager"
    assert result.value.roles == ()
    assert password_service.received_passwords == ["Strong#123"]
    assert factory.created[0].commits == 1
    assert factory.created[0].rollbacks == 0
    assert users.get_by_username(Username("manager")) is not None
    assert not hasattr(result.value, "password")
    assert not hasattr(result.value, "password_hash")


def test_create_user_handler_rejects_duplicate_username_and_rolls_back() -> None:
    users = InMemoryUserRepository()
    existing = User.create(
        Username("manager"),
        Email("old@sigesm.local"),
        PasswordHash(_VALID_ARGON2ID_HASH),
        full_name="Existing User",
    )
    users.add(existing)
    factory = InMemoryUserCreationUnitOfWorkFactory(users)
    password_service = _RecordingPasswordService()

    result = CreateUserHandler(factory, password_service).handle(
        CreateUserCommand("Manager User", "manager", "manager@sigesm.local", "Strong#123")
    )

    assert result.is_failure
    assert result.error == "Este login ja esta em uso."
    assert factory.created[0].rollbacks == 1
    assert password_service.received_passwords == []


def test_create_user_handler_rejects_duplicate_email_and_rolls_back() -> None:
    users = InMemoryUserRepository()
    existing = User.create(
        Username("oldmanager"),
        Email("manager@sigesm.local"),
        PasswordHash(_VALID_ARGON2ID_HASH),
        full_name="Existing User",
    )
    users.add(existing)
    factory = InMemoryUserCreationUnitOfWorkFactory(users)
    password_service = _RecordingPasswordService()

    result = CreateUserHandler(factory, password_service).handle(
        CreateUserCommand("Manager User", "manager", "manager@sigesm.local", "Strong#123")
    )

    assert result.is_failure
    assert result.error == "Este e-mail ja esta em uso."
    assert factory.created[0].rollbacks == 1
    assert password_service.received_passwords == []


def test_create_user_handler_rolls_back_commit_conflict() -> None:
    factory = _ConflictOnCommitFactory(InMemoryUserRepository())

    result = CreateUserHandler(factory, _RecordingPasswordService()).handle(
        CreateUserCommand("Manager User", "manager", "manager@sigesm.local", "Strong#123")
    )

    assert result.is_failure
    assert result.error == "Este login ou e-mail ja esta em uso."
    assert factory.unit_of_work.rollbacks == 1


def test_create_user_handler_rejects_invalid_username_email_and_password() -> None:
    handler = CreateUserHandler(
        InMemoryUserCreationUnitOfWorkFactory(InMemoryUserRepository()),
        _RecordingPasswordService(),
    )

    assert handler.handle(CreateUserCommand("User", "x", "u@sigesm.local", "Strong#123")).is_failure
    assert handler.handle(CreateUserCommand("User", "user", "invalid", "Strong#123")).is_failure
    assert handler.handle(CreateUserCommand("User", "user", "u@sigesm.local", "weak")).is_failure


def test_create_user_view_model_validates_confirmation_and_preserves_input() -> None:
    view_model = CreateUserViewModel(
        CreateUserService(
            InMemoryUserCreationUnitOfWorkFactory(InMemoryUserRepository()),
            _RecordingPasswordService(),
        )
    )
    view_model.update_input("full_name", "Manager User")
    view_model.update_input("username", "manager")
    view_model.update_input("email", "manager@sigesm.local")
    view_model.update_input("password", "Strong#123")
    view_model.update_input("password_confirmation", "Different#123")

    view_model.submit()

    assert view_model.field_errors["password_confirmation"] == (
        "A confirmacao da senha nao corresponde."
    )
    assert view_model.full_name == "Manager User"
    assert view_model.username == "manager"
    assert view_model.email == "manager@sigesm.local"


def test_create_user_view_model_emits_success_and_clears_passwords() -> None:
    view_model = CreateUserViewModel(
        CreateUserService(
            InMemoryUserCreationUnitOfWorkFactory(InMemoryUserRepository()),
            _RecordingPasswordService(),
        )
    )
    emitted: list[object] = []
    password_notifications: list[str] = []
    view_model.user_created.connect(lambda user: emitted.append(user))
    view_model.subscribe(
        lambda property_name: (
            password_notifications.append(property_name)
            if property_name in ("password", "password_confirmation")
            else None
        )
    )
    _fill_valid_view_model(view_model)
    password_notifications.clear()

    view_model.submit()

    assert len(emitted) == 1
    assert password_notifications == ["password", "password_confirmation"]
    assert not view_model.is_loading


def test_create_user_view_model_blocks_double_submit_while_loading() -> None:
    view_model = CreateUserViewModel(
        CreateUserService(
            InMemoryUserCreationUnitOfWorkFactory(InMemoryUserRepository()),
            _RecordingPasswordService(),
        )
    )
    view_model.update_input("full_name", "Manager User")
    view_model.update_input("username", "manager")
    view_model.update_input("email", "manager@sigesm.local")
    view_model.update_input("password", "Strong#123")
    view_model.update_input("password_confirmation", "Strong#123")
    view_model._set_loading(True)

    view_model.submit()

    assert view_model.is_loading


def test_user_form_dialog_save_button_follows_validity(qt_app: QApplication) -> None:
    view_model = CreateUserViewModel(
        CreateUserService(
            InMemoryUserCreationUnitOfWorkFactory(InMemoryUserRepository()),
            _RecordingPasswordService(),
        )
    )
    dialog = UserFormDialog(view_model)

    assert not dialog._save_button.isEnabled()
    _fill_valid_view_model(view_model)
    dialog._sync_state()

    assert dialog._save_button.isEnabled()
    dialog.reject()
    qt_app.processEvents()


def test_user_form_dialog_error_keeps_dialog_open(qt_app: QApplication) -> None:
    users = InMemoryUserRepository()
    users.add(
        User.create(
            Username("manager"),
            Email("old@sigesm.local"),
            PasswordHash(_VALID_ARGON2ID_HASH),
            full_name="Existing User",
        )
    )
    view_model = CreateUserViewModel(
        CreateUserService(InMemoryUserCreationUnitOfWorkFactory(users), _RecordingPasswordService())
    )
    dialog = UserFormDialog(view_model)
    _fill_valid_view_model(view_model)

    view_model.submit()

    assert dialog.result() == 0
    assert "login" in view_model.general_error.lower()
    dialog.reject()
    qt_app.processEvents()


def test_created_user_appears_in_listing() -> None:
    users = InMemoryUserRepository()
    create_service = CreateUserService(
        InMemoryUserCreationUnitOfWorkFactory(users),
        _RecordingPasswordService(),
    )
    listing_service = UserListingService(InMemoryUserListingRepository(users))

    create_service.create_user(
        CreateUserCommand("Manager User", "manager", "manager@sigesm.local", "Strong#123")
    )
    listed = listing_service.list_users(ListUsersQuery())

    assert listed.is_success
    assert tuple(item.login for item in listed.value.items) == ("manager",)
    assert listed.value.items[0].name == "Manager User"


def test_sqlalchemy_user_creation_persists_and_protects_duplicates(
    identity_session_factory: DatabaseSessionFactory,
) -> None:
    factory = SqlAlchemyUserCreationUnitOfWorkFactory(identity_session_factory)
    service = CreateUserService(factory, _RecordingPasswordService())

    created = service.create_user(
        CreateUserCommand("Manager User", "manager", "manager@sigesm.local", "Strong#123")
    )
    duplicate = service.create_user(
        CreateUserCommand("Other User", "manager", "other@sigesm.local", "Strong#123")
    )

    assert created.is_success
    assert duplicate.is_failure
    with identity_session_factory.create() as session:
        assert session.query(UserModel).count() == 1


def test_sqlalchemy_unit_of_work_translates_integrity_error(
    identity_session_factory: DatabaseSessionFactory,
) -> None:
    unit_of_work = SqlAlchemyUserCreationUnitOfWorkFactory(identity_session_factory).create()

    with unit_of_work:
        unit_of_work.users.add(
            User.create(
                Username("manager"),
                Email("manager@sigesm.local"),
                PasswordHash(_VALID_ARGON2ID_HASH),
                full_name="Manager User",
            )
        )
        unit_of_work.commit()

    with pytest.raises(IntegrityError):
        with identity_session_factory.create() as session:
            session.add(
                UserModel(
                    id="duplicate-1",
                    full_name="Other User",
                    username="manager",
                    email="other@sigesm.local",
                    password_hash=_VALID_ARGON2ID_HASH,
                    active=True,
                    failed_login_attempts=0,
                    locked_until=None,
                    created_at=User.create(
                        Username("tempuser"),
                        Email("tempuser@sigesm.local"),
                        PasswordHash(_VALID_ARGON2ID_HASH),
                    ).created_at,
                    updated_at=User.create(
                        Username("tempuser2"),
                        Email("tempuser2@sigesm.local"),
                        PasswordHash(_VALID_ARGON2ID_HASH),
                    ).updated_at,
                )
            )
            session.commit()


def _fill_valid_view_model(view_model: CreateUserViewModel) -> None:
    view_model.update_input("full_name", "Manager User")
    view_model.update_input("username", "manager")
    view_model.update_input("email", "manager@sigesm.local")
    view_model.update_input("password", "Strong#123")
    view_model.update_input("password_confirmation", "Strong#123")

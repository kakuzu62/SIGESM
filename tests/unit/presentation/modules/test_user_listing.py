from __future__ import annotations

from domain.identity.entities import User
from domain.identity.value_objects import Email, PasswordHash, Username
from infrastructure.identity import InMemoryUserRepository
from presentation.modules.user_management.application import UserListingService
from presentation.modules.user_management.application.common import PagedResult, SortDirection
from presentation.modules.user_management.application.queries.list_users import (
    ListUsersHandler,
    ListUsersQuery,
    UserListItemDTO,
)
from presentation.modules.user_management.infrastructure.repositories import (
    InMemoryUserListingRepository,
)
from presentation.modules.user_management.presentation.models import UserTableModel
from presentation.modules.user_management.presentation.viewmodels import UserListViewModel
from shared.kernel.result import Result

_VALID_ARGON2ID_HASH = (
    "$argon2id$v=19$m=65536,t=3,p=4$"
    "c2lnZXNtX3Rlc3Rfc2FsdA$"
    "F5agQp7LdbYQlwU++q7RrA3y8nY5jD9O81jHT2e66eE"
)


class _FailingUserListingService(UserListingService):
    def __init__(self) -> None:
        self.received_queries: list[ListUsersQuery] = []

    def list_users(self, query: ListUsersQuery) -> Result[PagedResult[UserListItemDTO]]:
        self.received_queries.append(query)
        return Result.failure("Falha ao carregar usuarios.")


class _SwitchingUserListingService(UserListingService):
    def __init__(self, successful_page: PagedResult[UserListItemDTO]) -> None:
        self._successful_page = successful_page
        self._calls = 0

    def list_users(self, query: ListUsersQuery) -> Result[PagedResult[UserListItemDTO]]:
        self._calls += 1
        if self._calls == 1:
            return Result.success(self._successful_page)
        return Result.failure("Falha ao carregar usuarios.")


def test_list_users_handler_returns_paged_users() -> None:
    repository = _repository_with_users("admin", "operator")
    handler = ListUsersHandler(repository)

    result = handler.handle(ListUsersQuery(page=1, page_size=1))

    assert result.is_success
    assert result.value.total == 2
    assert len(result.value.items) == 1


def test_list_users_handler_rejects_page_zero() -> None:
    handler = ListUsersHandler(_repository_with_users("admin"))

    result = handler.handle(ListUsersQuery(page=0))

    assert result.is_failure
    assert result.error == "Page must be greater than zero."


def test_list_users_handler_rejects_invalid_page_size() -> None:
    handler = ListUsersHandler(_repository_with_users("admin"))

    result = handler.handle(ListUsersQuery(page_size=0))

    assert result.is_failure
    assert result.error == "Page size must be between 1 and 100."


def test_list_users_handler_rejects_invalid_sort_field() -> None:
    handler = ListUsersHandler(_repository_with_users("admin"))

    result = handler.handle(ListUsersQuery(sort_by="password_hash"))

    assert result.is_failure
    assert result.error == "Sort field is not supported."


def test_list_users_handler_searches_users() -> None:
    repository = _repository_with_users("admin", "operator")
    handler = ListUsersHandler(repository)

    result = handler.handle(ListUsersQuery(filter_text="oper"))

    assert result.is_success
    assert tuple(item.login for item in result.value.items) == ("operator",)


def test_list_users_handler_returns_empty_search_result() -> None:
    repository = _repository_with_users("admin", "operator")
    handler = ListUsersHandler(repository)

    result = handler.handle(ListUsersQuery(filter_text="missing"))

    assert result.is_success
    assert result.value.items == ()
    assert result.value.total == 0


def test_list_users_handler_returns_partial_last_page() -> None:
    repository = _repository_with_users("alpha", "bravo", "charlie")
    handler = ListUsersHandler(repository)

    result = handler.handle(ListUsersQuery(page=2, page_size=2))

    assert result.is_success
    assert tuple(item.login for item in result.value.items) == ("charlie",)
    assert result.value.total_pages == 2


def test_list_users_handler_orders_descending() -> None:
    repository = _repository_with_users("admin", "operator")
    handler = ListUsersHandler(repository)

    result = handler.handle(ListUsersQuery(sort_by="login", direction=SortDirection.DESC))

    assert result.is_success
    assert tuple(item.login for item in result.value.items) == ("operator", "admin")


def test_user_list_view_model_loads_and_changes_page() -> None:
    view_model = UserListViewModel(
        UserListingService(_repository_with_users("alpha", "bravo", "charlie"))
    )
    changes: list[str] = []
    view_model.subscribe(changes.append)

    view_model.load()
    view_model.change_page(1)

    assert view_model.total == 3
    assert view_model.page == 1
    assert "users" in changes
    assert "page" in changes
    assert "total" in changes
    assert "total_pages" in changes
    assert "error_message" in changes


def test_user_list_view_model_searches() -> None:
    view_model = UserListViewModel(UserListingService(_repository_with_users("admin", "operator")))

    view_model.search("admin")

    assert tuple(item.login for item in view_model.users) == ("admin",)


def test_user_list_view_model_toggles_sort_direction() -> None:
    view_model = UserListViewModel(UserListingService(_repository_with_users("admin", "operator")))

    view_model.sort("login")
    first_order = tuple(item.login for item in view_model.users)
    view_model.sort("login")
    second_order = tuple(item.login for item in view_model.users)

    assert first_order == ("operator", "admin")
    assert second_order == ("admin", "operator")


def test_user_list_view_model_preserves_users_and_reports_error_on_failure() -> None:
    successful_page = _repository_with_users("admin").list_users(ListUsersQuery())
    view_model = UserListViewModel(_SwitchingUserListingService(successful_page))
    view_model.load()
    users_before_error = view_model.users
    changes: list[str] = []
    view_model.subscribe(changes.append)

    view_model.load()

    assert view_model.users == users_before_error
    assert view_model.error_message == "Falha ao carregar usuarios."
    assert changes.count("error_message") == 1


def test_user_list_view_model_notifies_loading_state() -> None:
    view_model = UserListViewModel(UserListingService(_repository_with_users("admin")))
    states: list[bool] = []

    def capture(property_name: str) -> None:
        if property_name == "is_loading":
            states.append(view_model.is_loading)

    view_model.subscribe(capture)

    view_model.load()

    assert states == [True, False]
    assert not view_model.is_loading


def test_user_list_view_model_emits_new_user_event() -> None:
    view_model = UserListViewModel(UserListingService(_repository_with_users("admin")))
    emitted: list[bool] = []
    view_model.new_user_requested.connect(lambda: emitted.append(True))

    view_model.request_new_user()

    assert emitted == [True]


def test_user_list_view_model_emits_edit_user_event() -> None:
    view_model = UserListViewModel(UserListingService(_repository_with_users("admin")))
    view_model.load()
    emitted: list[UserListItemDTO] = []
    view_model.edit_user_requested.connect(lambda user: emitted.append(user))

    view_model.request_edit_user(view_model.users[0])

    assert tuple(user.login for user in emitted) == ("admin",)


def test_user_list_view_model_ignores_edit_without_selection() -> None:
    view_model = UserListViewModel(UserListingService(_repository_with_users("admin")))
    emitted: list[UserListItemDTO] = []
    view_model.edit_user_requested.connect(lambda user: emitted.append(user))

    view_model.request_edit_user(None)

    assert emitted == []


def test_user_table_model_displays_user_data() -> None:
    result = _repository_with_users("admin").list_users(ListUsersQuery())
    model = UserTableModel()

    model.set_items(result.items)

    assert model.rowCount() == 1
    assert model.columnCount() == 6
    assert model.data(model.index(0, 0)) == "admin"


def test_user_table_model_handles_empty_data() -> None:
    model = UserTableModel()

    model.set_items(())

    assert model.rowCount() == 0
    assert model.item_at(0) is None


def test_user_list_item_dto_does_not_expose_sensitive_data() -> None:
    item = _repository_with_users("admin").list_users(ListUsersQuery()).items[0]

    assert not hasattr(item, "password")
    assert not hasattr(item, "password_hash")
    assert not hasattr(item, "token")


def _repository_with_users(*usernames: str) -> InMemoryUserListingRepository:
    users = InMemoryUserRepository()
    for username in usernames:
        users.add(
            User.create(
                Username(username),
                Email(f"{username}@sigesm.local"),
                PasswordHash(_VALID_ARGON2ID_HASH),
            )
        )
    return InMemoryUserListingRepository(users)

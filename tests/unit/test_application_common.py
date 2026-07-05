from __future__ import annotations

import pytest

from application.common.filters import FilterExpression, FilterGroup, FilterOperator
from application.common.ordering import Ordering, SortDirection
from application.common.pagination import PageResult, Pagination
from core.exceptions.validation import ValidationException


def test_pagination_calculates_offsets_and_page_metadata() -> None:
    pagination = Pagination(page=2, page_size=10)
    page = PageResult(items=("a", "b"), total_items=21, page=2, page_size=10)

    assert pagination.offset == 10
    assert page.total_pages == 3
    assert page.has_next is True
    assert page.has_previous is True


def test_application_common_objects_validate_empty_fields() -> None:
    with pytest.raises(ValidationException):
        Pagination(page=0)

    with pytest.raises(ValidationException):
        Ordering(field="")

    with pytest.raises(ValidationException):
        FilterExpression(field=" ", operator=FilterOperator.EQUALS, value="x")


def test_filter_group_empty_returns_empty_expression_tuple() -> None:
    group = FilterGroup.empty()

    assert group.expressions == ()
    assert Ordering(field="name", direction=SortDirection.DESC).direction == SortDirection.DESC

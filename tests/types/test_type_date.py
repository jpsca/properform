from datetime import date

import pytest

from proper_form.types import type_date


VALID_DATES = [
    ("2019-05-29", date(2019, 5, 29)),
    ("2019-5-29", date(2019, 5, 29)),
    ("2999-12-31", date(2999, 12, 31)),
    ("1970-01-01", date(1970, 1, 1)),
    ("1970-1-1", date(1970, 1, 1)),
    ("1-01-1", date(1, 1, 1)),
]

INVALID_DATES = [
    "",
    "qwertyuiop",
    "2019/05/29",
    "2019-13-01",
    "2019-02-31",
    "2019-02-99",
    "-02-31",
    "02-31",
    "999999999-02-13",
]


@pytest.mark.parametrize("value, expected", VALID_DATES)
def test_type_url_valid(value, expected):
    assert type_date(value) == expected


@pytest.mark.parametrize("value", INVALID_DATES)
def test_type_url_invalid(value):
    assert type_date(value) is None

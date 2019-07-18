import pytest

from proper_form.types import type_url


VALID_URLS = [
    ("http://example.com", "http://example.com"),
    ("example.com", "http://example.com"),
    ("example.pe", "http://example.pe"),
    ("https://example.com", "https://example.com"),
    ("example.com/a/b/c", "http://example.com/a/b/c"),
    ("mañana.co/yes", "http://mañana.co/yes"),
    ("Königsgäßchen.com", "http://königsgäßchen.com"),
    ("localhost:5000/login", "http://localhost:5000/login"),
    ("127.0.0.1", "http://127.0.0.1"),
]

INVALID_URLS = [
    "",
    "http//google.com",
    "http:://google.com",
    "http:google.com",
    "http:///google.com",
    "127..0.0.1",
]


@pytest.mark.parametrize("value, expected", VALID_URLS)
def test_type_url_valid(value, expected):
    assert type_url(value) == expected


@pytest.mark.parametrize("value", INVALID_URLS)
def test_type_url_invalid(value):
    assert type_url(value) is None


def test_type_url_tld():
    assert type_url("localhost", require_tld=True) is None
    assert type_url("localhost", require_tld=False) == "http://localhost"

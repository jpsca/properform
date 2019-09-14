import pytest

from proper_form.ftypes import type_hex_color


VALID_COLORS = [
    ("#2868c7", "#2868c7"),
    ("#FFF", "#ffffff"),
    ("#F2a", "#ff22aa"),
    ("#f2aa", "#ff22aaaa"),

    ("123", "#112233"),
    ("123456", "#123456"),

    ("rgb(0,0,0)", "#000000"),
    ("rgb(0, 0 ,0)", "#000000"),
    ("rgb( 0, 0 ,0 )", "#000000"),

    ("rgb(40,104,199)", "#2868c7"),
    ("rgba(40,104,199,0.5)", "#2868c780"),
    ("rgba(0,0,0)", "#000000"),
]

INVALID_COLORS = [
    "",
    "qwertyuiop",

    "1",
    "12",
    "12345",
    "#f",
    "#ff",
    "#abcde",
    "#g2e",
    "#ggff00",

    "rgb(256,0,0)",
    "rgb(0,-1,0)",
    "rgba(0,0,0,9)",
]


@pytest.mark.parametrize("value, expected", VALID_COLORS)
def test_type_hex_color_valid(value, expected):
    assert type_hex_color(value) == expected


@pytest.mark.parametrize("value", INVALID_COLORS)
def test_type_hex_color_invalid(value):
    assert type_hex_color(value) is None

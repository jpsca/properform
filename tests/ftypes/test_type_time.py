from datetime import time

import pytest

from hyperform.ftypes import type_time


VALID_TIMES = [
    ("4:20", time(4, 20, 0)),
    ("4:20 am", time(4, 20, 0)),
    ("4:20 pm", time(16, 20, 0)),
    ("4:20am", time(4, 20, 0)),
    ("4:20pm", time(16, 20, 0)),
    ("4:20:13am", time(4, 20, 13)),
    ("0:0:0 am", time(0, 0, 0)),
    ("00:00:00 am", time(0, 0, 0)),
    ("00:00:00", time(0, 0, 0)),
    ("4:20 PM", time(16, 20, 0)),
    ("4:20 p.m.", time(16, 20, 0)),
    ("16:20", time(16, 20, 0)),
    ("4:20:15 pm", time(16, 20, 15)),
    ("16:20:23", time(16, 20, 23)),
    ("4", time(4, 0, 0)),
    ("4 am", time(4, 0, 0)),
    ("4 pm", time(16, 0, 0)),
    ("12m", time(12, 0, 0)),
    ("12 m", time(12, 0, 0)),
    ("12 am", time(12, 0, 0)),
    # weird but valid
    ("0:0 pm", time(12, 0, 0)),
    ("00:00:00 pm", time(12, 0, 0)),
]

INVALID_TIMES = [
    "",
    "qwertyuiop",
    "2019-05-29",
    "4:60 pm",
    "13:10 pm",
    "13:10 m",
    "13:10 dc",
    "4:20:60",
    "4:20:60 pm",
    "12:10 m",
]


@pytest.mark.parametrize("value, expected", VALID_TIMES)
def test_type_hex_color_valid(value, expected):
    assert type_time(value) == expected


@pytest.mark.parametrize("value", INVALID_TIMES)
def test_type_hex_color_invalid(value):
    assert type_time(value) is None

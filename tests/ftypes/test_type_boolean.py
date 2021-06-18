import pytest

from hyperform.ftypes import type_boolean


TRUE_VALUES = ["1", "-1", "nu-hu", "foobar", "very false", "not a chance", "maybe"]

FALSE_VALUES = [
    "",
    "0",
    None,
    "None",
    "none",
    "no",
    "NO",
    "No",
    "nO",
    "Nope",
    "nah",
    "off",
    "Off",
    False,
    "false",
    "False",
]


@pytest.mark.parametrize("value", TRUE_VALUES)
def test_type_boolean_true(value):
    assert type_boolean(value)


@pytest.mark.parametrize("value", FALSE_VALUES)
def test_type_boolean_false(value):
    assert not type_boolean(value)

import pytest

import proper_form.fields as f


def test_text_as_input():
    field = f.Text(name="name")
    field.input_values = ["hello"]
    expected = '<input name="name" type="text" value="hello">'
    assert field.as_input() == expected


def test_text_as_input_no_value():
    field = f.Text(name="name")
    expected = '<input name="name" type="text" value="">'
    assert field.as_input() == expected


def test_text_as_input_attributes():
    field = f.Text(name="name")
    expected = '<input data-id="2" name="name" type="text" value="" extra>'
    assert field.as_input(data_id=2, extra=True) == expected


def test_text_as_input_required():
    field = f.Text(name="name", required=True)
    expected = '<input name="name" type="text" value="" required>'
    assert field.as_input() == expected


def test_text_as_input_with_label():
    field = f.Text(name="name")
    expected = (
        '<label for="name">Hello World</label>\n'
        '<input name="name" type="text" value="">'
    )
    assert field.as_input(label="Hello World") == expected


def test_text_as_input_with_label_and_custom_id():
    field = f.Text(name="name")
    expected = (
        '<label for="hello2">Hello World</label>\n'
        '<input id="hello2" name="name" type="text" value="">'
    )
    assert field.as_input(id="hello2", label="Hello World") == expected


def test_text_as_input_with_custom_type():
    field = f.Text(name="name")
    field.input_values = ["hello"]
    expected = '<input name="name" type="meh" value="hello">'
    assert field.as_input(type="meh") == expected


DEFAULT_INPUT_TYPES = [
    (f.Date, "date"),
    (f.Email, "email"),
    (f.File, "file"),
    (f.Float, "number"),
    (f.HexColor, "color"),
    (f.Integer, "number"),
    (f.Month, "month"),
    (f.Password, "password"),
    (f.Time, "time"),
    (f.URL, "url"),
]


@pytest.mark.parametrize("Field, expected_type", DEFAULT_INPUT_TYPES)
def test_default_input_types(Field, expected_type):
    field = Field(name="meh")
    expected = '<input name="meh" type="{}" value="">'.format(expected_type)
    assert field.as_input() == expected

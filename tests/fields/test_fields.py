from datetime import date, time, datetime
import pytest

from proper_form import fields as f


TEST_DATA = [
    (
        f.Date,
        "1973-09-11", date(1973, 9, 11), "invalid",
        "Date must have a YYYY-MM-dd format.",
    ),
    (
        f.Email,
        "abc@def.com", "abc@def.com", "invalid",
        "Doesn‘t look like a valid e-mail.",
    ),
    (
        f.HexColor,
        "#fef", "#ffeeff", "invalid",
        "Enter color in #hex, rgb() or rgba() format.",
    ),
    (
        f.Integer,
        "123", 123, "invalid",
        "Not a valid integer.",
    ),
    (
        f.Float,
        "123.2", 123.2, "invalid",
        "Not a valid float number.",
    ),
    (
        f.Time,
        "5:34 am", time(5, 34, 0), "invalid",
        "Enter a time in a 12h or 24h format.",
    ),
    (
        f.URL,
        "example.com", "http://example.com", "inv..alid",
        "Doesn‘t look like a valid URL.",
    ),
]


@pytest.mark.parametrize("Field, valid, expected, invalid, error", TEST_DATA)
def test_fields(Field, valid, expected, invalid, error):
    field = Field()

    assert field.validate([valid]) == expected
    assert field.error is None
    assert field.error_value is None

    assert field.validate([invalid]) is None
    assert field.error == error
    assert field.error_value == invalid


@pytest.mark.parametrize("Field, _valid, _expected, invalid, _error", TEST_DATA)
def test_required_filtered_values(Field, _valid, _expected, invalid, _error):
    field = Field(required=True, strict=False)

    assert field.validate([invalid]) is None
    assert field.error == "This field is required."


@pytest.mark.parametrize("Field, valid, expected, invalid, error", TEST_DATA)
def test_fields_single(Field, valid, expected, invalid, error):
    field = Field()

    assert field.validate([valid, valid, invalid]) == expected
    assert field.error is None
    assert field.error_value is None

    assert field.validate([invalid, valid, valid]) is None
    assert field.error == error
    assert field.error_value == invalid


@pytest.mark.parametrize("Field, valid, expected, invalid, error", TEST_DATA)
def test_fields_multiple(Field, valid, expected, invalid, error):
    field = Field(multiple=True)

    assert field.validate([valid, valid, valid]) == [expected, expected, expected]
    assert field.error is None
    assert field.error_value is None

    assert field.validate([valid, invalid, valid]) is None
    assert field.error == error
    assert field.error_value == invalid


@pytest.mark.parametrize("Field, valid, _expected, invalid, _error", TEST_DATA)
def test_fields_single_not_strict(Field, valid, _expected, invalid, _error):
    field = Field(strict=False)

    assert field.validate([invalid]) is None
    assert field.error is None
    assert field.error_value is None


@pytest.mark.parametrize("Field, valid, expected, invalid, _error", TEST_DATA)
def test_fields_multiple_not_strict(Field, valid, expected, invalid, _error):
    field = Field(multiple=True, strict=False)

    assert field.validate([valid, invalid, valid]) == [expected, expected]
    assert field.error is None
    assert field.error_value is None


def test_text():
    field = f.Text()
    assert field.validate(["lorem", "ipsum"]) == "lorem"
    assert field.error is None
    assert field.error_value is None

    field = f.Text(multiple=True)
    assert field.validate(["lorem", "ipsum"]) == ["lorem", "ipsum"]


def test_boolean():
    field = f.Boolean()

    assert field.validate(["on"]) is True
    assert field.error is None
    assert field.error_value is None

    assert field.validate([""]) is False
    assert field.error is None
    assert field.error_value is None


def test_boolean_single():
    field = f.Boolean()
    assert field.validate(["on", "yes", "no"]) is True
    assert field.error is None
    assert field.error_value is None

    assert field.validate(["", "yes", "1"]) is False
    assert field.error is None
    assert field.error_value is None


def test_boolean_multiple():
    field = f.Boolean(multiple=True)
    assert field.validate(["on", "yes", "no"]) == [True, True, False]
    assert field.error is None
    assert field.error_value is None

    assert field.validate(["", "yes", "1"]) == [False, True, True]
    assert field.error is None
    assert field.error_value is None


def test_splitted_date_time():
    field = f.SplittedDateTime()

    assert field.validate(["1973-09-11", "5:34 pm"]) == datetime(1973, 9, 11, 17, 34, 0)
    assert field.error is None
    assert field.error_value is None

    assert field.validate(["1973-09-11"]) == datetime(1973, 9, 11, 0, 0, 0)
    assert field.error is None
    assert field.error_value is None

    assert field.validate(["invalid"]) is None
    assert field.error == "Invalid type."
    assert field.error_value == ("invalid", "00:00")

    assert field.validate(["invalid", "5:34 pm"]) is None
    assert field.error == "Invalid type."
    assert field.error_value == ("invalid", "5:34 pm")


def test_splitted_date_time_single():
    field = f.SplittedDateTime()
    result = field.validate([
        "2018-05-05", "16:30",
        "2019-05-05", "16:30",
    ])
    assert result == datetime(2018, 5, 5, 16, 30, 0)
    assert field.error is None
    assert field.error_value is None


def test_splitted_date_time_multiple():
    field = f.SplittedDateTime(multiple=True)
    result = field.validate([
        "2018-05-05", "16:30",
        "2019-05-05", "16:30",
    ])
    expected = [
        datetime(2018, 5, 5, 16, 30, 0),
        datetime(2019, 5, 5, 16, 30, 0),
    ]
    assert result == expected
    assert field.error is None
    assert field.error_value is None


def test_splitted_date_time_single_not_strict():
    field = f.SplittedDateTime(strict=False)

    assert field.validate(["invalid"]) is None
    assert field.error is None
    assert field.error_value is None


def test_splitted_date_time_multiple_not_strict():
    field = f.SplittedDateTime(multiple=True, strict=False)

    result = field.validate([
        "2018-05-05", "16:30",
        "invalid", "lalala",
    ])
    expected = [
        datetime(2018, 5, 5, 16, 30, 0),
    ]
    assert result == expected
    assert field.error is None
    assert field.error_value is None


def test_splitted_fields_cannot_be_a_collection():
    with pytest.raises(AssertionError):
        f.SplittedDateTime(collection=True)

    with pytest.raises(AssertionError):
        f.Splitted(collection=True)


def test_splitted_fields_take_all_values():
    class MyLittleSplitted(f.Splitted):
        def _typecast_values(self, values):
            self.called_with = values[:]
            return values

    field = MyLittleSplitted()
    assert field.validate(["a", "b", "c", "d"]) == "a"
    assert field.called_with == ["a", "b", "c", "d"]

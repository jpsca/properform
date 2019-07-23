from datetime import date, time, datetime
import pytest

from proper_form import fields as f


TEST_DATA = [
    (
        f.Date,
        "1573-09-11",
        date(1573, 9, 11),
        "invalid",
        "Date must have a YYYY-MM-dd format.",
    ),
    (
        f.Email,
        "abc@def.com",
        "abc@def.com",
        "invalid",
        "Doesn‘t look like a valid e-mail.",
    ),
    (
        f.HexColor,
        "#fef",
        "#ffeeff",
        "invalid",
        "Enter color in #hex, rgb() or rgba() format.",
    ),
    (
        f.Integer,
        "123",
        123,
        "invalid",
        "Not a valid integer."
    ),
    (
        f.Float,
        "123.2",
        123.2,
        "invalid",
        "Not a valid float number."
    ),
    (
        f.Month,
        "1973-05",
        date(1973, 5, 1),
        "invalid",
        "Month must have a YYYY-MM format.",
    ),
    (
        f.Time,
        "5:34 am",
        time(5, 34, 0),
        "invalid",
        "Enter a time in a 12h or 24h format.",
    ),
    (
        f.URL,
        "example.com",
        "http://example.com",
        "inv..alid",
        "Doesn‘t look like a valid URL.",
    ),
]


@pytest.mark.parametrize("Field, valid, expected, invalid, error", TEST_DATA)
def test_fields(Field, valid, expected, invalid, error):
    field = Field()

    field.input_values = [valid]
    assert field.validate() == expected
    assert field.error is None
    assert field.error_value is None

    field.input_values = [invalid]
    assert field.validate() is None
    assert field.error == error
    assert field.error_value == invalid


@pytest.mark.parametrize("Field, _valid, _expected, invalid, _error", TEST_DATA)
def test_required_filtered_values(Field, _valid, _expected, invalid, _error):
    field = Field(required=True, strict=False)

    field.input_values = [invalid]
    assert field.validate() is None
    assert field.error == "This field is required."


@pytest.mark.parametrize("Field, valid, expected, invalid, error", TEST_DATA)
def test_field_single(Field, valid, expected, invalid, error):
    field = Field()

    field.input_values = [valid]
    assert field.validate() == expected
    assert field.error is None
    assert field.error_value is None


TEST_DATA_PREPARE = [
    (
        f.Date,
        ["1973-09-11"],
        date(1973, 9, 11)
    ),
    (
        f.Integer,
        ["123"],
        123
    ),
    (
        f.Float,
        ["123.2"],
        123.2
    ),
    (
        f.Month,
        ["1973-05"],
        date(1973, 5, 1)
    ),
    (
        f.SplittedDateTime,
        ["1973-09-11", "5:34 AM"],
        datetime(1973, 9, 11, 5, 34, 0)
    ),
    (
        f.SplittedDateTime,
        ["1973-09-11", "4:20:17 PM"],
        datetime(1973, 9, 11, 16, 20, 17),
    ),
    (
        f.Time,
        ["5:34 AM"],
        time(5, 34, 0)
    ),
    (
        f.Time,
        ["4:20:17 PM"],
        time(16, 20, 17)
    ),
]


@pytest.mark.parametrize("Field, expected, object_value", TEST_DATA_PREPARE)
def test_fields_prepare(Field, expected, object_value):
    field = Field()

    field.object_value = object_value
    assert field.values == expected
    assert field.validate() == object_value
    assert field.error is None
    assert field.error_value is None


@pytest.mark.parametrize("Field, valid, expected, invalid, error", TEST_DATA)
def test_fields_multiple(Field, valid, expected, invalid, error):
    field = Field(multiple=True)

    field.input_values = [valid, valid, valid]
    assert field.validate() == [expected, expected, expected]
    assert field.error is None
    assert field.error_value is None

    field.input_values = [valid, invalid, valid]
    assert field.validate() is None
    assert field.error == error
    assert field.error_value == invalid


@pytest.mark.parametrize("Field, valid, _expected, invalid, _error", TEST_DATA)
def test_fields_single_not_strict(Field, valid, _expected, invalid, _error):
    field = Field(strict=False)

    field.input_values = [invalid]
    assert field.validate() is None
    assert field.error is None
    assert field.error_value is None


@pytest.mark.parametrize("Field, valid, expected, invalid, _error", TEST_DATA)
def test_fields_multiple_not_strict(Field, valid, expected, invalid, _error):
    field = Field(multiple=True, strict=False)

    field.input_values = [valid, invalid, valid]
    assert field.validate() == [expected, expected]
    assert field.error is None
    assert field.error_value is None


def test_text():
    field = f.Text()
    field.input_values = ["lorem", "ipsum"]
    assert field.validate() == "lorem"
    assert field.error is None
    assert field.error_value is None

    field = f.Text(multiple=True)
    field.input_values = ["lorem", "ipsum"]
    assert field.validate() == ["lorem", "ipsum"]


def test_boolean():
    field = f.Boolean()

    field.input_values = ["on"]
    assert field.validate() is True
    assert field.error is None
    assert field.error_value is None

    field.input_values = [""]
    assert field.validate() is False
    assert field.error is None
    assert field.error_value is None


def test_boolean_single():
    field = f.Boolean()
    field.input_values = ["on", "yes", "no"]
    assert field.validate() is True
    assert field.error is None
    assert field.error_value is None

    field.input_values = ["", "yes", "1"]
    assert field.validate() is False
    assert field.error is None
    assert field.error_value is None


def test_boolean_multiple():
    field = f.Boolean(multiple=True)
    field.input_values = ["on", "yes", "no"]
    assert field.validate() == [True, True, False]
    assert field.error is None
    assert field.error_value is None

    field.input_values = ["", "yes", "1"]
    assert field.validate() == [False, True, True]
    assert field.error is None
    assert field.error_value is None


def test_splitted_date_time():
    field = f.SplittedDateTime()

    field.input_values = ["1973-09-11", "5:34 pm"]
    assert field.validate() == datetime(1973, 9, 11, 17, 34, 0)
    assert field.error is None
    assert field.error_value is None

    field.input_values = ["1973-09-11"]
    assert field.validate() == datetime(1973, 9, 11, 0, 0, 0)
    assert field.error is None
    assert field.error_value is None

    field.input_values = ["invalid"]
    assert field.validate() is None
    assert field.error == "Invalid type."
    assert field.error_value == ("invalid", "00:00")

    field.input_values = ["invalid", "5:34 pm"]
    assert field.validate() is None
    assert field.error == "Invalid type."
    assert field.error_value == ("invalid", "5:34 pm")


def test_splitted_date_time_single():
    field = f.SplittedDateTime()
    field.input_values = ["2018-05-05", "16:30", "2019-05-05", "16:30"]
    result = field.validate()
    assert result == datetime(2018, 5, 5, 16, 30, 0)
    assert field.error is None
    assert field.error_value is None


def test_splitted_date_time_multiple():
    field = f.SplittedDateTime(multiple=True)
    field.input_values = ["2018-05-05", "16:30", "2019-05-05", "16:30"]
    result = field.validate()
    expected = [datetime(2018, 5, 5, 16, 30, 0), datetime(2019, 5, 5, 16, 30, 0)]
    assert result == expected
    assert field.error is None
    assert field.error_value is None


def test_splitted_date_time_single_not_strict():
    field = f.SplittedDateTime(strict=False)

    field.input_values = ["invalid"]
    assert field.validate() is None
    assert field.error is None
    assert field.error_value is None


def test_splitted_date_time_multiple_not_strict():
    field = f.SplittedDateTime(multiple=True, strict=False)

    field.input_values = ["2018-05-05", "16:30", "invalid", "lalala"]
    result = field.validate()
    expected = [datetime(2018, 5, 5, 16, 30, 0)]
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
    field.input_values = ["a", "b", "c", "d"]
    assert field.validate() == "a"
    assert field.called_with == ["a", "b", "c", "d"]

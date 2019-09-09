from datetime import datetime, date

import pytest

from proper_form import Date
from proper_form import DateTime
from proper_form import Field
from proper_form import Integer
from proper_form import validators as v


def test_base_validator_message():
    validator = v.Validator()
    assert validator.message == "Invalid value."
    assert v.Validator(message="custom").message == "custom"


def test_confirmed_message():
    validator = v.Confirmed()
    assert validator.message == "Values doesn't match."
    assert v.Confirmed(message="custom").message == "custom"


def test_longer_than_message():
    validator = v.LongerThan(5)
    assert validator.message == "Field must be at least 5 character long."
    assert v.LongerThan(5, message="custom").message == "custom"


def test_shorter_than_message():
    validator = v.ShorterThan(5)
    assert validator.message == "Field cannot be longer than 5 characters."
    assert v.ShorterThan(5, message="custom").message == "custom"


def test_less_than_message():
    validator = v.LessThan(10)
    assert validator.message == "Number must be less than 10."
    assert v.LessThan(10, message="custom").message == "custom"


def test_more_than_message():
    validator = v.MoreThan(10)
    assert validator.message == "Number must be greater than 10."
    assert v.MoreThan(10, message="custom").message == "custom"


def test_in_range_message():
    validator = v.InRange(1900, 2010)
    assert validator.message == "Number must be between 1900 and 2010."
    assert v.InRange(1900, 2010, message="custom").message == "custom"


def test_before_message():
    dt = datetime(2017, 7, 5)
    validator = v.Before(dt)
    assert validator.message == "Enter a valid date before 2017-07-05."
    assert v.Before(dt, message="custom").message == "custom"


def test_after_message():
    dt = datetime(2017, 7, 5)
    validator = v.After(dt)
    assert validator.message == "Enter a valid date after 2017-07-05."
    assert v.After(dt, message="custom").message == "custom"


def test_before_now_message():
    validator = v.BeforeNow()
    assert validator.message == "Enter a valid date in the past."
    assert v.BeforeNow(message="custom").message == "custom"


def test_after_now_message():
    validator = v.AfterNow()
    assert validator.message == "Enter a valid date in the future."
    assert v.AfterNow(message="custom").message == "custom"


DATA = [
    [Field, v.Validator(), ["lorem", "ipsum"], True],

    [Field, v.Confirmed(), ["password", "password"], True],
    [Field, v.Confirmed(), ["password", "password", "password"], True],
    [Field, v.Confirmed(), ["password"], False],
    [Field, v.Confirmed(), ["lorem", "ipsum"], False],
    [Field, v.Confirmed(), ["password", "nope", "password"], False],

    [Field, v.LongerThan(5), ["123456789"], True],
    [Field, v.LongerThan(5), ["12345"], True],
    [Field, v.LongerThan(5), ["abc"], False],
    [Field, v.LongerThan(5), ["123456789", "qwertyuiop", "lorem ipsum"], True],
    [Field, v.LongerThan(5), ["123456789", "abc", "lorem ipsum"], False],

    [Field, v.ShorterThan(5), ["123"], True],
    [Field, v.ShorterThan(5), ["12345"], True],
    [Field, v.ShorterThan(5), ["qwertyuiop"], False],
    [Field, v.ShorterThan(5), ["1234", "abc", "lorem"], True],
    [Field, v.ShorterThan(5), ["1234", "abcdefghijk", "lorem"], False],

    [Integer, v.LessThan(10), ["8"], True],
    [Integer, v.LessThan(10), ["10"], True],
    [Integer, v.LessThan(10), ["34"], False],
    [Integer, v.LessThan(10), ["4", "3", "5"], True],
    [Integer, v.LessThan(10), ["4", "3", "25"], False],

    [Integer, v.MoreThan(10), ["20"], True],
    [Integer, v.MoreThan(10), ["-1"], False],
    [Integer, v.MoreThan(10), ["20", "13", "25"], True],
    [Integer, v.MoreThan(10), ["8", "13", "25"], False],

    [Integer, v.InRange(1900, 2010), ["1979"], True],
    [Integer, v.InRange(1900, 2010), ["1900"], True],
    [Integer, v.InRange(1900, 2010), ["2010"], True],
    [Integer, v.InRange(1900, 2010), ["1820"], False],
    [Integer, v.InRange(1900, 2010), ["3000"], False],
    [Integer, v.InRange(1900, 2010), ["-1"], False],
    [Integer, v.InRange(1900, 2010), ["1979", "1984", "2009"], True],
    [Integer, v.InRange(1900, 2010), ["1979", "1984", "2019"], False],

    [Date, v.Before(datetime(2017, 7, 5)), ["1979-05-05"], True],
    [Date, v.Before(datetime(2017, 7, 5)), ["2019-07-16"], False],
    [Date, v.Before(date(2017, 7, 5)), ["1979-05-05"], True],
    [Date, v.Before(date(2017, 7, 5)), ["2019-07-16"], False],

    [Date, v.After(datetime(2017, 7, 5)), ["2019-07-16"], True],
    [Date, v.After(datetime(2017, 7, 5)), ["1979-05-05"], False],
    [Date, v.After(date(2017, 7, 5)), ["2019-07-16"], True],
    [Date, v.After(date(2017, 7, 5)), ["1979-05-05"], False],

    [Date, v.BeforeNow(), ["1821-07-28"], True],
    [Date, v.BeforeNow(), ["3000-01-01"], False],

    [Date, v.AfterNow(), ["3000-01-01"], True],
    [Date, v.AfterNow(), ["1821-07-28"], False],

    [DateTime, v.Before(datetime(2017, 7, 5)), ["1979-05-05"], True],
    [DateTime, v.Before(datetime(2017, 7, 5)), ["2019-07-16"], False],
    [DateTime, v.Before(date(2017, 7, 5)), ["1979-05-05"], True],
    [DateTime, v.Before(date(2017, 7, 5)), ["2019-07-16"], False],

    [DateTime, v.After(datetime(2017, 7, 5)), ["2019-07-16"], True],
    [DateTime, v.After(datetime(2017, 7, 5)), ["1979-05-05"], False],
    [DateTime, v.After(date(2017, 7, 5)), ["2019-07-16"], True],
    [DateTime, v.After(date(2017, 7, 5)), ["1979-05-05"], False],

    [DateTime, v.BeforeNow(), ["1821-07-28"], True],
    [DateTime, v.BeforeNow(), ["3000-01-01"], False],

    [DateTime, v.AfterNow(), ["3000-01-01"], True],
    [DateTime, v.AfterNow(), ["1821-07-28"], False],
]


@pytest.mark.parametrize("FieldClass, validator, input_values, result", DATA)
def test_validators(FieldClass, validator, input_values, result):
    field = FieldClass(validator)
    field.input_values = input_values
    assert bool(field.validate()) is result


DATE_VALIDATORS = [
    v.Before(datetime(2017, 7, 5)),
    v.After(datetime(2017, 7, 5)),
    v.BeforeNow(),
    v.AfterNow(),
]


@pytest.mark.parametrize("validator", DATE_VALIDATORS)
def test_fail_if_not_date(validator):
    field = Integer(validator)
    field.input_values = ["1979"]
    with pytest.raises(AssertionError):
        field.validate()

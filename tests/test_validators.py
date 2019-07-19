from datetime import datetime, date

from proper_form import validators as v


def test_base_validator():
    validator = v.Validator()
    assert validator.message == "Invalid value."
    assert v.Validator(message="custom").message == "custom"

    assert validator(["lorem", "ipsum"])


def test_confirmed():
    validator = v.Confirmed()
    assert validator.message == "Values doesn't match."
    assert v.Confirmed(message="custom").message == "custom"

    assert validator(["password", "password"])
    assert validator(["password", "password", "password"])

    assert not validator(["password", "nope", "password"])


def test_longer_than():
    validator = v.LongerThan(5)
    assert validator.message == "Field must be at least 5 character long."
    assert v.LongerThan(5, message="custom").message == "custom"

    assert validator(["123456789"])
    assert validator(["12345"])
    assert not validator(["abc"])

    assert validator(["123456789", "qwertyuiop", "lorem ipsum"])
    assert not validator(["123456789", "abc", "lorem ipsum"])


def test_shorter_than():
    validator = v.ShorterThan(5)
    assert validator.message == "Field cannot be longer than 5 characters."
    assert v.ShorterThan(5, message="custom").message == "custom"

    assert validator(["123"])
    assert validator(["12345"])
    assert not validator(["qwertyuiop"])

    assert validator(["1234", "abc", "lorem"])
    assert not validator(["1234", "abcdefghijk", "lorem"])


def test_less_than():
    validator = v.LessThan(10)
    assert validator.message == "Number must be less than 10."
    assert v.LessThan(10, message="custom").message == "custom"

    assert validator([8])
    assert validator([10])
    assert not validator([34])

    assert validator([4, 3, 5])
    assert not validator([4, 3, 25])


def test_more_than():
    validator = v.MoreThan(10)
    assert validator.message == "Number must be greater than 10."
    assert v.MoreThan(10, message="custom").message == "custom"

    assert validator([20])
    assert not validator([-1])

    assert validator([20, 13, 25])
    assert not validator([8, 13, 25])


def test_in_range():
    validator = v.InRange(1900, 2010)
    assert validator.message == "Number must be between 1900 and 2010."
    assert v.InRange(1900, 2010, message="custom").message == "custom"

    assert validator([1979])
    assert validator([1900])
    assert validator([2010])

    assert not validator([1820])
    assert not validator([3000])
    assert not validator([-1])

    assert validator([1979, 1984, 2009])
    assert not validator([1979, 1984, 2019])


def test_before_datetime():
    dt = datetime(2017, 7, 5)
    validator = v.Before(dt)
    assert validator.message == "Enter a valid date before 2017-07-05."
    assert v.Before(dt, message="custom").message == "custom"

    assert validator([datetime(1979, 5, 5)])
    assert not validator([datetime(2019, 7, 16)])


def test_before_date():
    dt = date(2017, 7, 5)
    validator = v.Before(dt)

    assert validator([datetime(1979, 5, 5)])
    assert not validator([datetime(2019, 7, 16)])


def test_after_datetime():
    dt = datetime(2017, 7, 5)
    validator = v.After(dt)
    assert validator.message == "Enter a valid date after 2017-07-05."
    assert v.After(dt, message="custom").message == "custom"

    assert validator([datetime(2019, 7, 16)])
    assert not validator([datetime(1979, 5, 5)])


def test_after_date():
    dt = date(2017, 7, 5)
    validator = v.After(dt)

    assert validator([datetime(2019, 7, 16)])
    assert not validator([datetime(1979, 5, 5)])


def test_before_now():
    validator = v.BeforeNow()
    assert validator.message == "Enter a valid date in the past."
    assert v.BeforeNow(message="custom").message == "custom"

    assert validator([datetime(1821, 7, 28)])
    assert not validator([datetime(3000, 1, 1)])


def test_after_now():
    validator = v.AfterNow()
    assert validator.message == "Enter a valid date in the future."
    assert v.AfterNow(message="custom").message == "custom"

    assert validator([datetime(3000, 1, 1)])
    assert not validator([datetime(1821, 7, 28)])

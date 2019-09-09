import datetime
from itertools import groupby


__all__ = (
    "Validator",
    "Confirmed",
    "LongerThan",
    "ShorterThan",
    "LessThan",
    "MoreThan",
    "InRange",
    "Before",
    "After",
    "BeforeNow",
    "AfterNow",
)


class Validator(object):
    """Base field Validator.

    message (str):
        Error message to raise in case of a validation error.

    """

    message = "Invalid value."

    def __init__(self, message=None):
        if message is not None:
            self.message = message

    def test(self, value):
        return True

    def __call__(self, values):
        for value in values:
            if not self.test(value):
                return False
        return True


class Confirmed(Validator):
    """Validates that a value is identical every time has been repeated.
    Classic use is for password confirmation fields.

    message (str):
        Error message to raise in case of a validation error.

    """

    message = "Values doesn't match."

    def __call__(self, values):
        if len(values) < 2:
            return False
        g = groupby(values)
        return next(g, True) and not next(g, False)


class LongerThan(Validator):
    """Validates the length of a value is longer or equal than minimum.

    length (int):
        The minimum required length of the value.

    message (str):
        Error message to raise in case of a validation error.

    """

    message = "Field must be at least %s character long."

    def __init__(self, length, message=None):
        assert isinstance(length, int)
        self.length = length
        if message is None:
            message = self.message % (length,)
        self.message = message

    def test(self, value):
        return len(value) >= self.length


class ShorterThan(Validator):
    """Validates the length of a value is shorter or equal than maximum.

    length (int):
        The maximum allowed length of the value.

    message (str):
        Error message to raise in case of a validation error.

    """

    message = "Field cannot be longer than %s characters."

    def __init__(self, length, message=None):
        assert isinstance(length, int)
        self.length = length
        if message is None:
            message = self.message % (length,)
        self.message = message

    def test(self, value):
        return len(value) <= self.length


class LessThan(Validator):
    """Validates that a value is less or equal than another.
    This will work with integers, floats, decimals and strings.

    value (int|float):
        The maximum value acceptable.

    message (str):
        Error message to raise in case of a validation error.

    """

    message = "Number must be less than %s."

    def __init__(self, value, message=None):
        self.value = value
        if message is None:
            message = self.message % (value,)
        self.message = message

    def test(self, value):
        return value <= self.value


class MoreThan(Validator):
    """Validates that a value is greater or equal than another.
    This will work with any integers, floats, decimals and strings.

    value (int|float):
        The minimum value acceptable.

    message (str):
        Error message to raise in case of a validation error.

    """

    message = "Number must be greater than %s."

    def __init__(self, value, message=None):
        self.value = value
        if message is None:
            message = self.message % (value,)
        self.message = message

    def test(self, value):
        return value >= self.value


class InRange(Validator):
    """Validates that a value is of a minimum and/or maximum value.
    This will work with integers, floats, decimals and strings.

    minval (int|float):
        The minimum value acceptable.

    maxval (int|float):
        The maximum value acceptable.

    message (str):
        Error message to raise in case of a validation error.

    """

    message = "Number must be between %s and %s."

    def __init__(self, minval, maxval, message=None):
        self.minval = minval
        self.maxval = maxval
        if message is None:
            message = self.message % (minval, maxval)
        self.message = message

    def test(self, value):
        if value < self.minval:
            return False
        if value > self.maxval:
            return False
        return True


class Before(Validator):
    """Validates than the date happens before another.

    date (date|datetime):
        The latest valid date.

    message (str):
        Error message to raise in case of a validation error.
    """

    message = "Enter a valid date before %s."

    def __init__(self, dt, message=None):
        assert isinstance(dt, datetime.date)
        if not isinstance(dt, datetime.datetime):
            dt = datetime.datetime(dt.year, dt.month, dt.day)
        self.dt = dt
        if message is None:
            message = self.message % "{}-{:02d}-{:02d}".format(dt.year, dt.month, dt.day)
        self.message = message

    def test(self, value):
        assert isinstance(value, datetime.date)
        if not isinstance(value, datetime.datetime):
            value = datetime.datetime(value.year, value.month, value.day)
        return value <= self.dt


class After(Validator):
    """Validates than the date happens after another.

    date (date|datetime):
        The soonest valid date.

    message (str):
        Error message to raise in case of a validation error.
    """

    message = "Enter a valid date after %s."

    def __init__(self, dt, message=None):
        assert isinstance(dt, datetime.date)
        if not isinstance(dt, datetime.datetime):
            dt = datetime.datetime(dt.year, dt.month, dt.day)
        self.dt = dt
        if message is None:
            message = self.message % "{}-{:02d}-{:02d}".format(dt.year, dt.month, dt.day)
        self.message = message

    def test(self, value):
        assert isinstance(value, datetime.date)
        if not isinstance(value, datetime.datetime):
            value = datetime.datetime(value.year, value.month, value.day)
        return value >= self.dt


class BeforeNow(Before):
    """Validates than the date happens before now.
    This will work with both date and datetime values.

    message (str):
        Error message to raise in case of a validation error.

    """

    message = "Enter a valid date in the past."

    def __init__(self, message=None):
        if message is not None:
            self.message = message

    def test(self, value):
        self.dt = datetime.datetime.utcnow()
        return super().test(value)


class AfterNow(After):
    """Validates than the date happens after now.
    This will work with both date and datetime values.

    message (str):
        Error message to raise in case of a validation error.

    """

    message = "Enter a valid date in the future."

    def __init__(self, message=None):
        if message is not None:
            self.message = message

    def test(self, value):
        self.dt = datetime.datetime.utcnow()
        return super().test(value)

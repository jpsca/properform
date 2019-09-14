from itertools import groupby
import datetime


__all__ = (
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


def validate_values(values, test, message):
    for value in values:
        if not test(value):
            return False, message
    return True


class Confirmed(object):
    """Validates that a value is identical every time has been repeated.
    Classic use is for password confirmation fields.

    message (str):
        Error message to raise in case of a validation error.

    """

    message = "Values doesn't match."

    def __init__(self, message=None):
        if message is not None:
            self.message = message

    def __call__(self, values):
        if len(values) < 2:
            return False
        g = groupby(values)
        if next(g, True) and not next(g, False):
            return True
        return False, self.message


class LongerThan(object):
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

    def __call__(self, values):
        def test(value):
            return len(value) >= self.length

        return validate_values(values, test, self.message)


class ShorterThan(object):
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

    def __call__(self, values):
        def test(value):
            return len(value) <= self.length

        return validate_values(values, test, self.message)


class LessThan(object):
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

    def __call__(self, values):
        def test(value):
            return value <= self.value

        return validate_values(values, test, self.message)


class MoreThan(object):
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

    def __call__(self, values):
        def test(value):
            return value >= self.value

        return validate_values(values, test, self.message)


class InRange(object):
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

    def __call__(self, values):
        def test(value):
            if value < self.minval:
                return False
            if value > self.maxval:
                return False
            return True

        return validate_values(values, test, self.message)


class Before(object):
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
            message = self.message % "{}-{:02d}-{:02d}".format(
                dt.year, dt.month, dt.day
            )
        self.message = message

    def __call__(self, values):
        def test(value):
            assert isinstance(value, datetime.date)
            if not isinstance(value, datetime.datetime):
                value = datetime.datetime(value.year, value.month, value.day)
            return value <= self.dt

        return validate_values(values, test, self.message)


class After(object):
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
            message = self.message % "{}-{:02d}-{:02d}".format(
                dt.year, dt.month, dt.day
            )
        self.message = message

    def __call__(self, values):
        def test(value):
            assert isinstance(value, datetime.date)
            if not isinstance(value, datetime.datetime):
                value = datetime.datetime(value.year, value.month, value.day)
            return value >= self.dt

        return validate_values(values, test, self.message)


class BeforeNow(object):
    """Validates than the date happens before now.
    This will work with both date and datetime values.

    message (str):
        Error message to raise in case of a validation error.

    """

    message = "Enter a valid date in the past."

    def __init__(self, message=None):
        if message is not None:
            self.message = message

    def __call__(self, values):
        v = Before(datetime.datetime.utcnow(), self.message)
        return v(values)


class AfterNow(object):
    """Validates than the date happens after now.
    This will work with both date and datetime values.

    message (str):
        Error message to raise in case of a validation error.

    """

    message = "Enter a valid date in the future."

    def __init__(self, message=None):
        if message is not None:
            self.message = message

    def __call__(self, values):
        v = After(datetime.datetime.utcnow(), self.message)
        return v(values)

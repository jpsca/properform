import datetime

from ..types import type_date
from ..types import type_time

from .base import BaseField, Splitted


__all__ = ("Date", "Time", "SplittedDateTime")


class Date(BaseField):
    """A simple date field formatted as `YYYY-MM-dd`. Example: "1980-07-28".
    """

    def type(self, value):
        return type_date(value)


class Time(BaseField):
    """A simple 12-hours time field, seconds optional. Examples: "5:03 AM", "11:00 PM",
    "4:20:16 PM".
    """

    def type(self, value):
        return type_time(value)


class SplittedDateTime(Splitted):
    """A Datetime field splitted in a date and a time field (with the same name).
    The first value is the date and the second one the time.
    """

    # We want to recieve multiple values, hence this is True, but to process
    # one values, so we inherit from `BaseField`.
    multi = True

    def type(self, values):
        date = type_date(values[0])
        time = type_time(values[1])
        return datetime.combine(date, time)

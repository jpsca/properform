import re
import datetime

from .bases import BaseField


__all__ = ("Date", "Time", )


class Date(BaseField):
    """A simple date field formatted as `YYYY-MM-dd`. Example: "1980-07-28".
    """

    def type(self, value):
        return value_to_date(value)


class Time(BaseField):
    """A simple 12-hours time field, seconds optional. Examples: "5:03 AM", "11:00 PM",
    "4:20:16 PM".
    """

    def type(self, value):
        return value_to_time(value)


class SpliitedDateTime(BaseField):
    """A Datetime field splitted in a date and a time field (with the same name).
    The first value is the date and the second one the time.
    """

    # We want to recieve multiple values, hence this is True, but to process
    # one values, so we inherit from `BaseField`.
    multi = True

    def type(self, values):
        date = value_to_date(values[0])
        time = value_to_time(values[1])
        return datetime.combine(date, time)


# --- Private ---

rx_time = re.compile(
    r"(?P<hour>[0-9]{1,2}):(?P<minute>[0-9]{1,2})(:(?P<second>[0-9]{1,2}))?\s?(?P<tt>am|pm)?",
    re.IGNORECASE,
)


def value_to_date(value):
    ldt = [int(f) for f in value.split("-")]
    return datetime.date(*ldt)


def value_to_time(value):
    match = rx_time.match(value.upper())
    if not match:
        return None

    gd = match.groupdict()
    hour = int(gd["hour"])
    minute = int(gd["minute"])
    second = int(gd["second"] or 0)
    if gd["tt"] == "PM":
        hour += 12

    return datetime.time(hour, minute, second)

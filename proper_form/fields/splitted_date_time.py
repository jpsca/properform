import datetime

from ..types import type_date
from ..types import type_time

from .splitted import Splitted


__all__ = ("SplittedDateTime", )


class SplittedDateTime(Splitted):
    """A Datetime field splitted in a date and a time field (with the same name).
    The first value is the date and the second one the time.
    """

    def type(self, values):
        date = type_date(values[0])
        time = type_time(values[1])
        return datetime.combine(date, time)

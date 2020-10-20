from datetime import datetime

from ..ftypes import type_date
from ..ftypes import type_time

from .text import Text


__all__ = ("DateTime",)


class DateTime(Text):
    """A simple date-time field formatted as `YYYY-MM-dd` with the time in 12 or
    24-hours format, seconds optional.

    Examples: "1980-07-28 5:03 AM", "2019-09-08 4:20:16 PM", "2019-09-08 16:34".
    """

    input_type = "date"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.error_messages.setdefault(
            "type",
            "DateTime must have a YYYY-MM-dd with time in 12h or 24h format,"
            " seconds optional.",
        )

    def prepare(self, object_value):
        return [
            self._prepare_date(object_value) + " " + self._prepare_time(object_value)
        ]

    def _prepare_date(self, object_value):
        return object_value.strftime("%Y-%m-%d")

    def _prepare_time(self, object_value):
        value = "{}:{:02d}".format(
            object_value.hour if object_value.hour <= 12 else object_value.hour - 12,
            object_value.minute,
        )
        if object_value.second:
            value += ":{:02d}".format(object_value.second)
        value += object_value.strftime(" %p")
        return value

    def type(self, value):
        if " " not in value:
            value += " 00:00"  # So it always has a time
        date_part, time_part = value.split(" ", maxsplit=1)
        return datetime.combine(type_date(date_part), type_time(time_part))

from ..types import type_time

from .field import Field


__all__ = ("Time", )


class Time(Field):
    """A simple 12-hours time field, seconds optional. Examples: "5:03 AM", "11:00 PM",
    "4:20:16 PM".
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.error_messages.setdefault(
            "type", "Enter a time in a 12h or 24h format."
        )

    def type(self, value):
        return type_time(value)

from ..types import type_time

from .text import Text


__all__ = ("Time", )


class Time(Text):
    """A simple 12-hours time field, seconds optional. Examples: "5:03 AM", "11:00 PM",
    "4:20:16 PM".
    """

    input_type = "time"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.error_messages.setdefault(
            "type", "Enter a time in a 12h or 24h format."
        )

    def prepare(self, object_value):
        return object_value.time().strftime("%r")

    def type(self, value):
        return type_time(value)

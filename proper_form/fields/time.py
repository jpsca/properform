from ..types import type_time

from .field import Field


__all__ = ("Time", )


class Time(Field):
    """A simple 12-hours time field, seconds optional. Examples: "5:03 AM", "11:00 PM",
    "4:20:16 PM".
    """

    type = type_time

from ..types import type_date

from .field import Field


__all__ = ("Date", )


class Date(Field):
    """A simple date field formatted as `YYYY-MM-dd`. Example: "1980-07-28".
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.error_messages.setdefault(
            "type", "Date must have a YYYY-MM-dd format."
        )

    def type(self, value):
        return type_date(value)

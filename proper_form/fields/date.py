from ..types import type_date

from .text import Text


__all__ = ("Date", )


class Date(Text):
    """A simple date field formatted as `YYYY-MM-dd`. Example: "1980-07-28".
    """

    input_type = "date"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.error_messages.setdefault(
            "type", "Date must have a YYYY-MM-dd format."
        )

    def prepare(self, object_value):
        return [object_value.strftime("%Y-%m-%d")]

    def type(self, value):
        return type_date(value)

from ..types import type_date

from .text import Text


__all__ = ("Month", )


class Month(Text):
    """A simple month field formatted as `YYYY-MM`. Example: "1980-07".
    """

    input_type = "month"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.error_messages.setdefault(
            "type", "Month must have a YYYY-MM format."
        )

    def prepare(self, object_value):
        return [object_value.strftime("%Y-%m")]

    def type(self, value):
        value = str(value or "") + "-01"
        return type_date(value)

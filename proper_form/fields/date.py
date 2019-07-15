from ..types import type_date

from .field import Field


__all__ = ("Date", )


class Date(Field):
    """A simple date field formatted as `YYYY-MM-dd`. Example: "1980-07-28".
    """

    type = type_date

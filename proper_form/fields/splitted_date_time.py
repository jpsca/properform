from datetime import datetime

from ..types import type_date
from ..types import type_time

from .splitted import Splitted


__all__ = ("SplittedDateTime", )


class SplittedDateTime(Splitted):
    """A Datetime field splitted in a date and a time field (with the same name).
    The first value is the date and the second one the time.
    """

    def prepare(self, object_value):
        return [self._prepare_date(object_value), self._prepare_time(object_value)]

    def _prepare_date(self, object_value):
        return object_value.strftime("%Y-%m-%d")

    def _prepare_time(self, object_value):
        value = "{}:{:02d}".format(
            object_value.hour if object_value.hour <= 12 else object_value.hour - 12,
            object_value.minute
        )
        if object_value.second:
            value += ":{:02d}".format(object_value.second)
        value += object_value.strftime(" %p")
        return value

    def _pre(self, values):
        if not self.multiple:
            return values[:2]
        return values

    def _typecast_values(self, values):
        pyvalues = []
        values.append("00:00")  # So it always has a time
        pairs = zip(values[::2], values[1::2])

        for date, time in pairs:
            try:
                pyvalue = datetime.combine(type_date(date), type_time(time))
            except (ValueError, TypeError, IndexError):
                pyvalue = None

            if pyvalue is None:
                if self.strict:
                    self._set_error("type")
                    self.error_value = (date, time)
                    return
                continue  # pragma: no cover
            pyvalues.append(pyvalue)
        return pyvalues

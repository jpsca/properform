import datetime
import re


__all__ = ("type_time", )

rx_noon = re.compile(r"^12\s*m?$", re.IGNORECASE)
rx_time = re.compile(
    r"^(?P<hour>[0-9]{1,2})(:(?P<minute>[0-9]{1,2}))?"
    r"(:(?P<second>[0-9]{1,2}))?\s*(?P<tt>am|pm)?$",
    re.IGNORECASE,
)


def type_time(value):
    if rx_noon.match(value):
        return datetime.time(12, 0, 0)

    value = value.upper()
    value = value.replace("P.M.", "PM").replace("A.M.", "AM")
    match = rx_time.match(value)
    if not match:
        return None

    gd = match.groupdict()
    hour = int(gd["hour"])
    minute = int(gd["minute"] or 0)
    second = int(gd["second"] or 0)
    if gd["tt"] == "PM":
        hour += 12

    try:
        return datetime.time(hour, minute, second)
    except (ValueError, TypeError):
        return None

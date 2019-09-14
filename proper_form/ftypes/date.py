import datetime


__all__ = ("type_date", )


def type_date(value):
    try:
        ldt = [int(f) for f in value.split("-")]
        return datetime.date(*ldt)
    except (ValueError, TypeError):
        return None

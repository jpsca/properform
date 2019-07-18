__all__ = ("type_boolean", )


default_false_values = ("", "none", "0", "no", "nope", "nah", "off", "false")


def type_boolean(value, false_values=default_false_values):
    if value.strip().lower() in false_values:
        return False
    return True
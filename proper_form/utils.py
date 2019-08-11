

__all__ = ("FakeMultiDict", "get_input_values", "get_object_value", )


class FakeMultiDict(dict):
    def getall(self, name):
        return []


def get_input_values(data, name):
    # - WebOb, Bottle, and Proper uses `getall`
    # - Django, Werkzeug, cgi.FieldStorage, etc. uses `getlist`
    # - CherryPy just gives you a dict with lists or values
    values = []
    for method in ("getall", "getlist"):
        if hasattr(data, method):
            values = getattr(data, method)(name)
            break
    else:
        values = data.get(name)

    # Some frameworks, like CherryPy, don't have a special method for
    # always returning a list of values.
    if values is None:
        return []
    if not isinstance(values, (list, tuple)):
        return [values]

    return values


def get_object_value(obj, name):
    # The object could be a also a dictionary
    # The field name could conflict with a native method
    # if `obj` is a dictionary instance
    if isinstance(obj, dict):
        return obj.get(name, None)
    return getattr(obj, name, None)

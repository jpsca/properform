

class FakeMultiDict(object):
    def getlist(self, name):
        return []


class Form(object):

    def __init__(self, input_data=None, object_data=None, prefix="", getall=None):
        input_data = FakeMultiDict() if input_data is None else input_data
        object_data = FakeMultiDict() if object_data is None else object_data
        if not isinstance(input_data, (list, tuple)):
            input_data = [input_data]
        self.input_data = input_data
        self.object_data = object_data

        self.prefix = prefix

        # `getall` is the name of the method to get the LIST of all values
        # with that name.
        # - Django, Werkzeug, cgi.FieldStorage, etc. uses `getlist`
        # - WebOb, Bottle, and Proper uses `getall`
        # - CherryPy just gives you a dict with lists or values
        if getall is None:
            for method in ("getlist", "getall", "get"):
                if hasattr(input_data[0], method):
                    getall = method
                    break
        self.getall = getall

        self._set_names()

    def _get_input_values(self, name):
        for data in self.input_data:
            values = getattr(data, self.getall)(name)
            if values:
                # Some frameworks (cough CherryPy) don't have a special method for
                # always returning a list of values.
                if not isinstance(values, (list, tuple)):
                    return [values]
                return values
        return []

    def _set_names(self):
        """ """

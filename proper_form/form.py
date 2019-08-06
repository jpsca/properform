from .fields import Field
from .form_set import FormSet


__all__ = ("Form", )


class FakeMultiDict(dict):
    def getall(self, name):
        return []


class Form(object):

    errors = None
    valid_data = None
    updated_fields = None

    def __init__(self, input_data=None, object_data=None, file_data=None, prefix=""):
        self.prefix = prefix or ""

        self._load_fields()
        self.load_object_data(object_data)
        self.load_input_data(input_data, file_data)

    def load_object_data(self, object_data=None):
        object_data = object_data or {}

        for name in self._fields:
            field = getattr(self, name)
            field.object_value = get_object_value(object_data, name)

        for name in self._formsets:
            formaset = getattr(self, name)
            formaset.load_object_data(get_object_value(object_data, name))

    def load_input_data(self, input_data=None, file_data=None):
        input_data = FakeMultiDict() if input_data is None else input_data
        file_data = FakeMultiDict() if file_data is None else file_data

        for name in self._fields:
            field = getattr(self, name)
            full_name = field.name
            field.input_values = get_input_values(input_data, full_name) \
                or get_input_values(file_data, full_name)

    @property
    def is_valid(self):
        if self.valid_data is None and self.errors is None:
            self.validate()
        return self.errors is None

    def validate(self):
        if self.errors is not None:
            return None
        if self.valid_data is not None:
            return self.valid_data

        self._reset()
        errors = {}
        valid_data = {}
        updated = []

        for name in self._fields:
            field = getattr(self, name)
            py_value = field.validate()

            if field.error:
                errors[name] = field.error
                continue

            valid_data[name] = py_value
            if field.updated:
                updated.append(name)

        for name in self._formsets:
            formset = getattr(self, name)
            py_value = formset.validate()

            if formset.error:
                errors[name] = formset.error
                continue

            valid_data[name] = py_value
            if formset.updated:
                updated.append(name)

        if errors:
            self.errors = errors
            return None

        self.valid_data = valid_data
        self.updated_fields = updated
        return valid_data

    # Private

    def _load_fields(self):
        fields = []
        formsets = []
        attrs = (
            "errors",
            "file_data",
            "input_data",
            "is_valid",
            "object_data",
            "prefix",
            "updated_fields",
            "valid_data",
            "validate",
        )
        for name in dir(self):
            if name.startswith("_") or name in attrs:
                continue
            attr = getattr(self, name)

            if isinstance(attr, Field):
                self._load_field(attr, name)
                fields.append(name)

            if isinstance(attr, FormSet):
                self._load_formset(name)
                formsets.append(name)

        self._fields = fields
        self._formsets = formsets

    def _load_field(self, field, name):
        if self.prefix:
            field.name = self.prefix + "." + name
        else:
            field.name = name
        if field.custom_prepare is None:
            field.custom_prepare = getattr(self, "prepare_" + name, None)
        if field.custom_clean is None:
            field.custom_clean = getattr(self, "clean_" + name, None)

    def _load_formset(self, formset, name):
        if self.prefix:
            formset.prefix = self.prefix + "." + name
        else:
            formset.prefix = name

    def _reset(self):
        self.errors = None
        self.valid_data = None
        self.updated_fields = None


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

from .constants import SEP, DELETED, ID
from .fields import Field
from .form_set import FormSet
from .utils import FakeMultiDict, get_input_values, get_object_value


__all__ = ("Form", )


class Form(object):

    updated_fields = None

    _id = None
    _is_valid = None
    _valid_data = None
    _fields = None
    _formsets = None
    _deleted = False

    def __init__(self, input_data=None, object_data=None, file_data=None, prefix=""):
        self.prefix = prefix or ""
        self._setup_fields()
        self.load_data(input_data, object_data, file_data)

    def load_data(self, input_data=None, object_data=None, file_data=None):
        self._reset()
        input_data = FakeMultiDict() if input_data is None else input_data
        file_data = FakeMultiDict() if file_data is None else file_data
        object_data = object_data or {}

        self._id = get_object_value(object_data, "id")

        _deleted = self.prefix + SEP + DELETED if self.prefix else DELETED
        if _deleted in input_data:
            self._deleted = True

        self._load_field_data(input_data, object_data, file_data)
        self._load_fieldset_data(input_data, object_data, file_data)

    @property
    def is_valid(self):
        if self._is_valid is None:
            self.validate()
        return self._is_valid

    def validate(self):
        if self._is_valid is False:
            return None
        if self._valid_data is not None:
            return self._valid_data

        self._reset()
        is_valid = True
        updated = []

        valid_data = {}
        if self._id is not None:
            valid_data[ID] = self._id
        if self._deleted:
            valid_data[DELETED] = True

        for name in self._fields:
            field = getattr(self, name)
            py_value = field.validate()

            if field.error:
                is_valid = False
                continue

            valid_data[name] = py_value
            if field.updated:
                updated.append(name)

        for name in self._formsets:
            formset = getattr(self, name)
            py_value = formset.validate()

            if not formset.is_valid:
                is_valid = False
                continue

            valid_data[name] = py_value
            if formset.updated:
                updated.append(name)

        self._is_valid = is_valid
        if is_valid:
            self._valid_data = valid_data
            self.updated_fields = updated
            return valid_data

    def _setup_fields(self):
        fields = []
        formsets = []
        attrs = (
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
                self._setup_field(attr, name)
                fields.append(name)

            if isinstance(attr, FormSet):
                self._setup_formset(attr, name)
                formsets.append(name)

        self._fields = fields
        self._formsets = formsets

    def _setup_field(self, field, name):
        if self.prefix:
            field.name = self.prefix + SEP + name
        else:
            field.name = name
        if field.custom_prepare is None:
            field.custom_prepare = getattr(self, "prepare_" + name, None)
        if field.custom_clean is None:
            field.custom_clean = getattr(self, "clean_" + name, None)

    def _setup_formset(self, formset, name):
        if self.prefix:
            formset.prefix = self.prefix + "." + name + SEP
        else:
            formset.prefix = name + SEP

    def _reset(self):
        self._is_valid = None
        self._valid_data = None
        self.updated_fields = None

    def _load_field_data(self, input_data, object_data, file_data):
        for name in self._fields:
            field = getattr(self, name)
            full_name = field.name
            field.object_value = get_object_value(object_data, name)
            field.input_values = get_input_values(input_data, full_name) \
                or get_input_values(file_data, full_name)

    def _load_fieldset_data(self, input_data, object_data, file_data):
        for name in self._formsets:
            formset = getattr(self, name)
            formset.load_data(
                input_data,
                get_object_value(object_data, name),
                file_data
            )

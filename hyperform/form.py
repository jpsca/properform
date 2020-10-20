from copy import copy

from markupsafe import Markup

from .constants import SEP, DELETED, ID
from .fields import Field
from .form_set import FormSet
from .utils import FakeMultiDict, get_input_values, get_object_value, get_html_attrs


__all__ = ("Form",)


class Form(object):

    error = None
    updated_fields = None
    prefix = None

    _id = None
    _model = None
    _is_valid = None
    _valid_data = None
    _fields = None
    _formsets = None
    _deleted = False
    _can_delete = False

    def __init__(
        self,
        input_data=None,
        object=None,
        file_data=None,
        *,
        prefix="",
        can_delete=False,
    ):
        self.prefix = prefix or ""
        self._can_delete = can_delete
        self._setup_fields()
        self.load_data(input_data, object, file_data)

    def __repr__(self):
        return f"{self.__class__.__name__}({self.prefix})"

    def load_data(self, input_data=None, object=None, file_data=None):
        self._is_valid = None
        self._valid_data = None
        self.updated_fields = None

        input_data = FakeMultiDict() if input_data is None else input_data
        file_data = FakeMultiDict() if file_data is None else file_data
        object = object or {}
        if isinstance(object, dict) or object is None:
            self._object = None
        else:
            self._object = object

        self._id = get_object_value(object, "id")

        if self._can_delete:
            _deleted = self.prefix + SEP + DELETED if self.prefix else DELETED
            if _deleted in input_data:
                self._deleted = True

        self._load_field_data(input_data, object, file_data)
        self._load_fieldset_data(input_data, object, file_data)

    def render_error(self, tag="div", **attrs):
        if not self.error:
            return ""

        attrs.setdefault("classes", "error")
        return Markup("<{tag} {attrs}>{error}</{tag}>".format(
            tag=tag,
            attrs=get_html_attrs(attrs),
            error=self.error,
        ))

    def validate(self):  # noqa: C901
        if self._is_valid is False:
            return None
        if self._valid_data is not None:
            return self._valid_data

        self.error = None
        is_valid = True
        updated = []
        valid_data = {}

        if self._id is not None:
            valid_data[ID] = self._id

        if self._deleted:
            self._is_valid = True
            self.updated_fields = updated
            valid_data[DELETED] = True
            self._valid_data = valid_data
            return self._valid_data

        for name in self._fields:
            field = getattr(self, name)
            py_value = field.validate()

            if field.error:
                is_valid = False
                self.error = field.error
                continue

            valid_data[name] = py_value
            if field.updated:
                updated.append(name)

        for name in self._formsets:
            formset = getattr(self, name)
            py_value = formset.validate()

            if not formset.validate():
                is_valid = False
                self.error = formset.error
                continue

            valid_data[name] = py_value
            if formset.updated:
                updated.append(name)

        self._is_valid = is_valid
        if is_valid:
            self._valid_data = valid_data
            self.updated_fields = updated
            return valid_data

    def save(self, **data):
        if not self.validate():
            return None

        data.update(self._valid_data)
        if not self._model:
            return data

        data.pop(ID, None)
        data.pop(DELETED, None)

        if self._object and self._deleted:
            self.delete_object()
            return None

        for name in self._formsets:
            formset = getattr(self, name)
            if formset.backref:
                data.pop(name, None)
                continue
            data[name] = formset.save()

        if self._object:
            obj = self.update_object(data)
        else:
            obj = self.create_object(data)

        for name in self._formsets:
            formset = getattr(self, name)
            if formset.backref is None:
                continue
            formset.save(parent=obj)

        return obj

    def create_object(self, data):  # pragma: no cover
        return data

    def update_object(self, data):
        for key, value in data.items():
            setattr(self._object, key, value)
        return self._object

    def delete_object(self):  # pragma: no cover
        pass

    def _setup_fields(self):
        fields = []
        formsets = []
        attrs = (
            "updated_fields",
            "prefix",
            "load_data",
            "validate",
            "save",
            "create_object",
            "update_object",
            "delete_object",
            "get_db_session",
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
        field = copy(field)
        setattr(self, name, field)
        if self.prefix:
            field.name = self.prefix + SEP + name
        else:
            field.name = name
        if field.custom_prepare is None:
            field.custom_prepare = getattr(self, "prepare_" + name, None)
        if field.custom_clean is None:
            field.custom_clean = getattr(self, "clean_" + name, None)

    def _setup_formset(self, formset, name):
        formset = copy(formset)
        setattr(self, name, formset)
        if self.prefix:
            formset.prefix = self.prefix + "." + name + SEP
        else:
            formset.prefix = name + SEP

    def _load_field_data(self, input_data, object, file_data):
        for name in self._fields:
            field = getattr(self, name)
            full_name = field.name
            input_values = get_input_values(
                input_data, full_name
            ) or get_input_values(file_data, full_name)
            object_value = get_object_value(object, name)
            field.load_data(input_values, object_value)

    def _load_fieldset_data(self, input_data, object, file_data):
        for name in self._formsets:
            formset = getattr(self, name)
            formset.load_data(
                input_data, get_object_value(object, name), file_data
            )

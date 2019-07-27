import re

from .field_renderable import FieldRenderable


__all__ = ("Field", )


default_error_messages = {
    "type": "Invalid type.",
    "required": "This field is required.",
    "min_num_values": "You need at least {num} values.",
    "max_num_values": "You can have at most {num} values.",
}


class Field(FieldRenderable):
    r"""

    Arguments are:

        collection (bool):
            This field takes an open number of values of the same kind.
            For example, a list of comma separated tags or email addresses.

        sep (str):
            If `collection` is True, string to separate each value (default is ",").
            Ignored otherwise

    """

    __slots__ = (
        "validators",
        "name",
        "required",
        "strict",
        "error_messages",
        "collection",
        "sep",
        "multiple",
        "min_num_values",
        "max_num_values",
        "extra",
    )

    deleted = False
    object_value = None
    input_values = None
    input_type = "text"

    error = None
    error_value = None
    updated = False

    def __init__(
        self,
        *validators,

        name=None,
        required=False,
        strict=True,
        error_messages=None,

        prepare=None,
        clean=None,

        collection=False,
        sep=",",
        multiple=False,
        min_num_values=None,
        max_num_values=None,

        **extra
    ):
        self.validators = validators
        self.name = name or ""
        self.required = required
        self.strict = strict
        self.error_messages = error_messages or {}

        self.custom_prepare = prepare
        self.custom_clean = clean

        self.collection = collection
        if collection:
            self.sep = sep
            multiple = False
        self.multiple = multiple

        if collection or multiple:
            self.min_num_values = min_num_values
            self.max_num_values = max_num_values

        self.extra = extra

    @property
    def values(self):
        if self.input_values is not None:
            return self.input_values
        if self.object_value is not None:
            return (self.custom_prepare or self.prepare)(self.object_value)
        return []

    @property
    def value(self):
        return self.values[0] if self.values else None

    def prepare(self, object_value):
        return [object_value]

    def clean(self, pyvalues):
        return pyvalues

    def validate(self):
        self._reset()
        values = [str(value).strip() for value in self.values or []]

        if not values:
            if self.required:
                self._set_error("required")
            return None

        values = self._pre(values)
        pyvalues = self._typecast_values(values)
        if self.error:
            return None

        # Typecasting with `strict=False` could've emptied the values without erroring.
        # An empty string is only an error if the field is required
        if (not pyvalues or pyvalues[0] == "") and self.required:
            self._set_error("required")
            return None

        self._validate_values(pyvalues)
        if self.error:
            return None

        pyvalues = self._post(pyvalues)
        value = (self.custom_clean or self.clean)(pyvalues)
        self.updated = value != self.object_value
        return value

    def type(self, value, **kwargs):
        return str(value)

    def _reset(self):
        self.error = None
        self.error_value = None
        self.updated = False

    def _pre(self, values):
        if self.collection:
            rxsep = r"\s*%s\s*" % re.escape(self.sep.strip())
            return re.split(rxsep, values[0])
        elif self.multiple:
            return values
        return values[:1]

    def _post(self, values):
        if self.collection:
            return self.sep.join(values)
        elif self.multiple:
            return values
        else:
            return values[0] if values else None

    def _typecast_values(self, values):
        pyvalues = []
        for value in values:
            try:
                pyvalue = self.type(value, **self.extra)
            except (ValueError, TypeError, IndexError):
                pyvalue = None

            if pyvalue is None:
                if self.strict:
                    self._set_error("type")
                    self.error_value = value
                    return
                continue  # pragma: no cover
            pyvalues.append(pyvalue)
        return pyvalues

    def _validate_values(self, pyvalues):
        if self.collection or self.multiple:
            num_values = len(pyvalues)
            if self.min_num_values is not None and self.min_num_values > num_values:
                self._set_error("min_num_values", num=self.min_num_values)
                return
            if self.max_num_values is not None and self.max_num_values < num_values:
                self._set_error("max_num_values", num=self.max_num_values)
                return

        for validator in self.validators:
            if not validator(pyvalues):
                self.error = validator.message
                return

    def _set_error(self, name, **kwargs):
        msg = self.error_messages.get(name) or default_error_messages.get(name, "")
        for key, repl in kwargs.items():
            msg = msg.replace("{" + key + "}", str(repl))
        self.error = msg or name

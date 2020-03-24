import re

from .field_renderable import FieldRenderable


__all__ = ("Field", )


default_error_messages = {
    "required": "This field is required.",
    "type": "Invalid type.",
    "min_num": "You need at least {num} values.",
    "max_num": "You can have at most {num} values.",
}

HARD_MAX_NUM = 1000


class Field(FieldRenderable):
    r"""

    Arguments are:

        *validators,

        name=None,
        required=False,
        strict=True,
        error_messages=None,

        prepare=None,
        clean=None,

        collection (bool):
            This field takes an open number of values of the same kind.
            For example, a list of comma separated tags or email addresses.

        sep (str):
            If `collection` is True, string to separate each value (default is ",").
            Ignored otherwise

        multiple=False,
        min_num=None,
        max_num=None,

        **extra


    """

    __slots__ = (
        "validators",
        "name",
        "required",
        "strict",
        "error_messages",
        "multiple",
        "min_num",
        "max_num",
        "collection",
        "sep",
        "extra",
    )

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

        multiple=False,
        min_num=None,
        max_num=None,
        collection=False,
        sep=",",

        prepare=None,
        clean=None,

        **extra
    ):
        self.validators = validators
        self.name = name or ""

        self.required = required
        self.strict = strict
        self.min_num = min_num
        if max_num is not None:
            max_num = min(max_num, HARD_MAX_NUM)
        self.max_num = max_num
        self.error_messages = error_messages or {}

        self.collection = collection
        if collection:
            self.sep = sep
            multiple = False
        self.multiple = multiple

        self.custom_prepare = prepare
        self.custom_clean = clean

        self.extra = extra

    def load_data(self, input_values=None, object_value=None):
        self.input_values = input_values
        self.object_value = object_value

    @property
    def values(self):
        if self.input_values:
            return self.input_values
        if self.object_value:
            return (self.custom_prepare or self.prepare)(self.object_value)
        return []

    @property
    def value(self):
        return self.values[0] if self.values else ""

    def prepare(self, object_value):
        return [object_value]

    def validate(self):
        self._reset()
        values = [str(value).strip() for value in self.input_values or []]

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

        pyvalue = self._post(pyvalues)
        if self.custom_clean:
            pyvalue = self.custom_clean(pyvalue)
        self.updated = pyvalue != self.object_value
        return pyvalue

    def type(self, value, **kwargs):
        return str(value)

    # Private

    def _reset(self):
        self.error = None
        self.error_value = None
        self.updated = False

    def _pre(self, values):
        if self.collection:
            rxsep = r"\s*%s\s*" % re.escape(self.sep.strip())
            all_values = []
            for value in values:
                all_values += re.split(rxsep, value)
            return all_values
        return values

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
        num_values = len(pyvalues)

        if self.min_num is not None and self.min_num > num_values:
            self._set_error("min_num", num=self.min_num)
            return

        if self.max_num is not None and self.max_num < num_values:
            self._set_error("max_num", num=self.max_num)
            return

        for validator in self.validators:
            message = "Invalid value"
            valid = validator(pyvalues)
            if valid not in (True, False):
                valid, message = valid

            if not valid:
                self.error = message
                return

    def _set_error(self, name, **kwargs):
        msg = self.error_messages.get(name) or default_error_messages.get(name, "")
        for key, repl in kwargs.items():
            msg = msg.replace("{" + key + "}", str(repl))
        self.error = msg or name

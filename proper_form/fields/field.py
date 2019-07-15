

__all__ = ("Field", )

default_error_messages = {
    "type": "Invalid type",
    "required": "This field is required",
    "min_num_values": "You need at least {num} values",
    "max_num_values": "You can have at most {num} values",
}


def identity(value):
    return value


class Field(object):
    r"""

    Arguments are:

        collection (bool):
            This field takes an open number of values of the same kind.
            For example, a list of comma separated tags or email addresses.

        sep (str):
            If `collection` is True, string to separate each value (default is ",").
            Ignored otherwise

    """

    # Object value
    value = None
    error = None
    strict = None
    multi = False
    type = None

    def __init__(
        self,
        type,
        *validators,

        name=None,
        required=False,
        strict=False,
        error_messages=None,

        prepare=identity,
        clean=identity,

        collection=False,
        sep=",",
        multiple=False,
        min_num_values=None,
        max_num_values=None,

        **extra
    ):
        self.error = None

        self.type = type or self.type
        self.validators = validators

        self.name = name

        self.required = required
        self.strict = strict
        self.error_messages = error_messages

        self.prepare = prepare
        self.clean = clean

        self.collection = collection
        if collection:
            self.sep = sep
            multiple = True
        self.multiple = multiple
        self.min_num_values = min_num_values
        self.max_num_values = max_num_values

        self.extra = extra

    def validate(self, values):
        values = self.prepare(values)

        if self.required and not values:
            self._set_error("required")
            return

        values = self._pre(values)

        pyvalues = self._typecast_values(value)
        if self.error:
            return

        if self.required and not pyvalues:
            self._set_error("required")
            return

        self._validate_values(pyvalues)
        if self.error:
            return

        pyvalues = self._post(pyvalues)
        return self.clean(pyvalues)

    def _pre(self, values):
        if self.collection:
            rxsep = r"\s*%s\s*" % re.escape(self.sep.strip())
            return re.split(values[0], rxsep)
        return values

    def _post(self, values):
        if collection:
            return self.sep.join(values)
        elif self.multiple:
            return values
        else:
            return values[0]

    def _typecast_values(self, values):
        pyvalues = []
        for value in values:
            try:
                value = self.type(value, **self.extra)
                pyvalues.append(value)
            except (ValueError, TypeError, IndexError):
                if self.strict:
                    self._set_error("type")
                    return
        return pyvalues

    def _validate_values(self, pyvalues):
        if self.multiple:
            num_values = len(pyvalues)
            if self.min_num_values is not None and self.min_num_values < num_values:
                self._set_error("min_num_values", num=min_num_values)
                return
            if self.max_num_values is not None and self.max_num_values > num_values:
                self._set_error("max_num_values", num=max_num_values)
                return

        for pyval in pyvalues:
            for validator in self.validators:
                if not validator(pyval):
                    self._set_error(validator.name)
                    return

    def _set_error(self, name, **kwargs):
        msg = self.error_messages.get(name) or self.default_error_messages.get(name)
        for key, repl in kwargs.items():
            msg = msg.replace("{" + key + "}", repl)
        self.error = msg or name

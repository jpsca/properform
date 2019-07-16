import re


__all__ = ("Field", )


default_error_messages = {
    "type": "Invalid type.",
    "required": "This field is required.",
    "min_num_values": "You need at least {num} values.",
    "max_num_values": "You can have at most {num} values.",
}


def identity(value, **kwargs):
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

    value = None  # Object value
    type = identity

    def __init__(
        self,
        *validators,

        name=None,
        required=False,
        strict=True,
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

        self.validators = validators

        self.name = name
        self.required = required
        self.strict = strict
        self.error_messages = error_messages or {}

        self.prepare = prepare
        self.clean = clean

        self.collection = collection
        if collection:
            self.sep = sep
            multiple = False
        self.multiple = multiple
        self.min_num_values = min_num_values
        self.max_num_values = max_num_values

        self.extra = extra
        self.clear_error()

    def clear_error(self):
        self.error = None
        self.error_value = None

    def validate(self, values):
        self.clear_error()

        values = self.prepare(values)

        if self.required and not values:
            self._set_error("required")
            return

        values = self._pre(values)

        pyvalues = self._typecast_values(values)
        if self.error:
            return

        # Typecasting with `strict=False` could've emptied the values without erroring.
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
        elif not self.multiple:
            return values[:1]
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
                continue
            pyvalues.append(pyvalue)
        return pyvalues

    def _validate_values(self, pyvalues):
        if self.multiple:
            num_values = len(pyvalues)
            if self.min_num_values is not None and self.min_num_values < num_values:
                self._set_error("min_num_values", num=self.min_num_values)
                return
            if self.max_num_values is not None and self.max_num_values > num_values:
                self._set_error("max_num_values", num=self.max_num_values)
                return

        for validator in self.validators:
            if not validator(pyvalues):
                self.error = validator.message
                return

    def _set_error(self, name, **kwargs):
        msg = self.error_messages.get(name) or default_error_messages.get(name, "")
        for key, repl in kwargs.items():
            msg = msg.replace("{" + key + "}", repl)
        self.error = msg or name

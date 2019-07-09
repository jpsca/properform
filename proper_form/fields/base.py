__all__ = ("BaseField", "Splitted")

default_error_messages = {
    "type": "Invalid type",
    "required": "This field is required",
}


def identity(value):
    return value


class BaseField(object):
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
        *,
        clean=identity,
        required=False,
        error_messages=None,
        strict=False,
        name=None,
        collection=False,
        sep=",",
        multiple=False,
        **extra
    ):
        self.error = None
        self.type = type or self.type
        self.validators = validators
        self.clean = clean
        self.required = required
        self.error_messages = error_messages
        self.name =
        self.collection = collection
        if collection:
            self.sep = sep
            multiple = True
        self.multiple = multiple
        self.extra = extra

    def validate(self, values):
        values = self.clean(values)

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

        return self._post(pyvalues)

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
                value = self.type(value)
                pyvalues.append(value)
            except (ValueError, TypeError, IndexError):
                if self.strict:
                    self._set_error("type")
                    return
        return pyvalues

    def _validate_values(self, pyvalues):
        for pyval in pyvalues:
            for validator in self.validators:
                if not validator(pyval):
                    self._set_error(validator.name)
                    return

    def _set_error(self, name):
        self.error = (
            self.error_messages.get(name)
            or self.default_error_messages.get(name)
            or name
        )


class Splitted(BaseField):
    """Doesn't allow `multiple` or `collection` to be True.
    """
    def __init__(self, *args, **kwargs):
        assert not kwargs.get("collection"), "A splitted field cannot be a collection."
        assert not kwargs.get("multiple"), "A splitted field cannot be `multiple`."
        super().__init__(*args, **kwargs)

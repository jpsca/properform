

__all__ = ("BaseField", "BaseMultiField", "Validates", "validates")

default_error_messages = {
    "type": "Invalid type",
    "required": "This field is required",
}


def identity(value):
    return value


class BaseField(object):

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
        **extra
    ):
        self.error = None
        self.type = type or self.type
        self.validators = validators
        self.clean = clean
        self.required = required
        self.error_messages = error_messages
        self.name = name
        self.extra = extra

    def validate(self, value):
        value = self.clean(value)
        value = self._pre(value)

        pyvalue = self._typecast_value(value)
        if self.error:
            return

        if self.required and not pyvalue:
            self._set_error("required")
            return

        self._validate_value(pyvalue)
        if self.error:
            return

        pyvalue = self._post(pyvalue)
        return pyvalue

    def _pre(self, value):
        return value

    def _post(self, value):
        return value

    def _typecast_value(self, value):
        try:
            return self.type(value)
        except (ValueError, TypeError):
            if self.strict:
                self._set_error("type")

    def _validate_value(self, pyvalue):
        for validator in self.validators:
            if not validator(pyvalue):
                self._set_error(validator.name)
                return

    def _set_error(self, name):
        self.error = (
            self.error_messages.get(name)
            or self.default_error_messages.get(name)
            or name
        )


class BaseMultiField(BaseField):

    multi = True

    def validate(self, values):
        pyvalues = self._typecast_values(values)
        if self.error:
            return

        if self.required and not pyvalues:
            self._set_error("required")
            return

        self._validate_values(pyvalues)
        if self.error:
            return

        return pyvalues

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


class Validates(BaseField):

    def __init__(self, type, *validators, only_if=None, unless=None, **kwargs):
        self.only_if = only_if
        self.unless = unless
        super().__init__(type, *validators, **kwargs)

    def __call__(self, value):
        if (not self.only_if or self.only_if()) and (not self.unless or not self.unless()):
            pyvalue = self.validates(value)
        if self.error:
            raise ValueError(self.error)
        return pyvalue


validates = Validates

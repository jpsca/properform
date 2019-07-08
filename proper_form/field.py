

__all__ = ("BaseField", "BaseMulti", "validates")

default_error_messages = {
    "type": "Invalid type",
    "required": "This field is required",
}


class BaseField(object):

    error = None
    strict = None
    multi = False

    def __init__(
        self,
        type,
        *validators,
        *,
        required=False,
        error_messages=None,
        strict=False,
        name=None,
        **ops
    ):
        self.error = None
        self.type = type
        self.validators = validators
        self.required = required
        self.error_messages = error_messages
        self.name = name
        self.ops = ops

    def validate(self, value):
        pyvalue = self._typecast_value(value)
        if self.error:
            return

        if self.required and not pyvalue:
            self._set_error("required")
            return

        self._validate_value(pyvalue)
        if self.error:
            return

        return pyvalue

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


class BaseMulti(BaseField):

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
            except (ValueError, TypeError):
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


def validates(name, type, *validators, *, required=False, strict=False, **kwargs):
    return BaseField(
        type,
        *validators,
        required=required,
        strict=strict,
        name=name,
        **kwargs
    )

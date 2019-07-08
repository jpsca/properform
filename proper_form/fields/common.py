from .bases import BaseField, BaseMultiField


__all__ = ("Text", "Integer", "Float", "Boolean", "Multiple")


class Text(BaseField):
    type = str


class Integer(BaseField):
    type = int


class Float(BaseField):
    type = float


class Boolean(BaseField):

    false_values = ("None", "", "0", "no", "off", "false")

    def type(self, value):
        if str(value).lower() in self.false_values:
            return False
        return True


class Multiple(BaseMultiField):
    type = int

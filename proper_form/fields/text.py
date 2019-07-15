from .field import Field


__all__ = ("Text", )


class Text(Field):

    def type(self, value):
        return str(value).strip()

from ..types import type_boolean

from .field import Field


__all__ = ("Boolean", )


class Boolean(Field):

    def type(self, value):
        return type_boolean(value)

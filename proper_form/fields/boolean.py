from ..ftypes import type_boolean

from .text import Text


__all__ = ("Boolean", )


class Boolean(Text):

    def type(self, value):
        return type_boolean(value)

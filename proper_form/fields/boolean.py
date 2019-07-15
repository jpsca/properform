from ..types import type_boolean

from .field import Field


__all__ = ("Boolean", )


class Boolean(Field):

    type = type_boolean

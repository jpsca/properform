from .field import Field


__all__ = ("Integer", "Float", )


class Integer(Field):
    type = int


class Float(Field):
    type = float

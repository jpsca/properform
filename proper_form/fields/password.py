from .text import Text


__all__ = ("Password", )


class Password(Text):

    input_type = "password"

    @property
    def values(self):
        return [""]

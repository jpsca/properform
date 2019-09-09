from .text import Text


__all__ = ("Splitted", )


class Splitted(Text):
    def __init__(self, *args, **kwargs):
        assert not kwargs.get("collection"), "A splitted field cannot be a collection."
        super().__init__(*args, **kwargs)

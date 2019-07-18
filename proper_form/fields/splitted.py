from .text import Text


__all__ = ("Splitted", )


class Splitted(Text):
    """Doesn't allow `multiple` or `collection` to be True.
    """
    def __init__(self, *args, **kwargs):
        assert not kwargs.get("collection"), "A splitted field cannot be a collection."
        super().__init__(*args, **kwargs)

    def _pre(self, values):
        return values

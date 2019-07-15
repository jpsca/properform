from .field import Field


__all__ = ("Splitted", )


class Splitted(Field):
    """Doesn't allow `multiple` or `collection` to be True.
    """
    def __init__(self, *args, **kwargs):
        assert not kwargs.get("collection"), "A splitted field cannot be a collection."
        assert not kwargs.get("multiple"), "A splitted field cannot be `multiple`."
        super().__init__(*args, **kwargs)

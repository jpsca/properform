from .text import Text


__all__ = ("Float", )


class Float(Text):

    input_type = "number"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.error_messages.setdefault("type", "Not a valid float number.")

    def type(self, value):
        return float(value)

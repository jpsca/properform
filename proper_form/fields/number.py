from .text import Text


__all__ = ("Integer", "Float", )


class Integer(Text):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.error_messages.setdefault("type", "Not a valid integer.")

    def type(self, value):
        return int(value)


class Float(Text):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.error_messages.setdefault("type", "Not a valid float number.")

    def type(self, value):
        return float(value)

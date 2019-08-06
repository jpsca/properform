

__all__ = ("FormSet", )


default_error_messages = {
    "min_num": "Please submit at least {num} forms.",
    "max_num": "Please submit at most {num} forms.",
}

HARD_MAX_NUM = 1000


class FormSet(object):

    __slots__ = (
        "FormClass",
        "extra",
        "min_num",
        "max_num",
        "can_delete",
        "can_create",
        "error_messages",
    )

    prefix = ""
    error = None
    updated = False

    def __init__(
        self,
        FormClass,
        *,
        extra=0,
        min_num=None,
        max_num=None,
        can_delete=True,
        can_create=True,
        error_messages=None,
    ):
        self.FormClass = FormClass
        self.extra = extra
        self.min_num = min_num
        if max_num is not None:
            max_num = min(max_num, HARD_MAX_NUM)
        self.max_num = max_num

    def load_object_data(self, object_data=None):
        pass

    def load_input_data(self, input_data=None, file_data=None):
        pass

    def validate(self):
        self._reset()
        pass

    # Private

    def _reset(self):
        self.error = None
        self.updated = False

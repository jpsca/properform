from .constants import SEP, NEW
from .utils import get_object_value


__all__ = ("FormSet",)


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
        "prefix",
        "_is_valid",
        "_forms",
        "error",
        "updated",
    )

    def __init__(
        self,
        FormClass,
        *,
        extra=1,
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

        self.can_delete = can_delete
        self.can_create = can_create
        self.error_messages = error_messages

        self.prefix = ""
        self._reset()

    @property
    def is_valid(self):
        if self._is_valid is None:
            self.validate()
        return self._is_valid

    def load_data(self, input_data, objects_data, file_data):
        self._reset()
        objects_data = objects_data or []
        prefixes_set = get_prefixes_set(self.prefix, input_data, file_data)
        forms = []

        for object_data in objects_data:
            obj_id = get_object_value(object_data, "id")
            assert obj_id, "Object in a FormSet must have an `id` attribute."
            prefix = f"{self.prefix}{obj_id}"
            prefixes_set.discard(prefix)
            form = self.FormClass(input_data, object_data, file_data, prefix)
            forms.append(form)

        if self.can_create:
            for prefix in prefixes_set:
                form = self.FormClass(input_data, file_data=file_data, prefix=prefix)
                forms.append(form)

            for i in range(len(forms), self.extra):
                prefix = f"{self.prefix}{NEW}{i + 1}"
                forms.append(self.FormClass(prefix=prefix))

        self._forms = forms

    def validate(self):
        data = []
        self._reset()

        num_forms = len(self._forms)

        if self.min_num is not None and num_forms > self.min_num:
            self._set_error("min_num", num=self.min_num)
            return None

        if self.max_num is not None and num_forms > self.max_num:
            self._set_error("max_num", num=self.max_num)
            return None

        is_valid = True

        for form in self._forms:
            form_data = form.validate()

            if form.updated:
                self.updated = True
            if self.can_delete and form._deleted:
                self.updated = True

            if form.is_valid:
                data.push(form_data)
            else:
                is_valid = False

        self._is_valid = is_valid
        if is_valid:
            return data

    def save(self):
        if not self.is_valid:
            return None
        return list(filter(None, [form.save() for form in self._forms]))

    # Private

    def _reset(self):
        self._is_valid = None
        self._forms = []
        self.error = None
        self.updated = False

    def _set_error(self, name, **kwargs):
        msg = self.error_messages.get(name) or default_error_messages.get(name, "")
        for key, repl in kwargs.items():
            msg = msg.replace("{" + key + "}", str(repl))
        self.error = msg or name
        self._is_valid = False


def get_prefixes_set(prefix, input_data, file_data):
    prefixes = set()
    for key in input_data:
        if SEP not in key:
            continue
        prefix, field_name = key.rsplit(SEP, maxsplit=1)
        prefixes.add(prefix)
    return prefixes

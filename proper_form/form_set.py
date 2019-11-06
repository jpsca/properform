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
        "backref",
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
        backref=None,
        extra=1,
        min_num=None,
        max_num=None,
        can_delete=True,
        can_create=True,
        error_messages=None,
    ):
        self.FormClass = FormClass
        self.backref = backref
        self.extra = extra
        self.min_num = min_num
        if max_num is not None:
            max_num = min(max_num, HARD_MAX_NUM)
        self.max_num = max_num

        self.can_delete = can_delete
        self.can_create = can_create
        self.error_messages = error_messages or {}

        self.prefix = ""
        self._is_valid = None
        self.error = None
        self.updated = False
        self._forms = []

    def __len__(self):
        return len(self._forms)

    def __getitem__(self, index):
        return self._forms[index]

    def load_data(self, input_data, objects_data, file_data):
        self._is_valid = None
        self._forms = []
        self.error = None
        self.updated = False

        objects_data = objects_data or []
        prefixes = get_prefixes(self.prefix, input_data, file_data)
        forms = []

        for object in objects_data:
            obj_id = get_object_value(object, "id")
            assert obj_id, "Object in a FormSet must have an `id` attribute."
            prefix = f"{self.prefix}{obj_id}"
            if prefix in prefixes:
                prefixes.remove(prefix)
            form = self.FormClass(
                input_data,
                object,
                file_data,
                prefix=prefix,
                can_delete=self.can_delete
            )
            forms.append(form)

        if self.can_create:
            for prefix in prefixes:
                form = self.FormClass(input_data, file_data=file_data, prefix=prefix)
                forms.append(form)

            for i in range(len(forms), self.extra):
                prefix = f"{self.prefix}{NEW}{i + 1}"
                forms.append(self.FormClass(prefix=prefix))

        self._forms = forms

    def validate(self):
        data = []

        num_forms = len(self._forms)

        if self.min_num is not None and num_forms < self.min_num:
            self._set_error("min_num", num=self.min_num)
            self._is_valid = False
            return None

        if self.max_num is not None and num_forms > self.max_num:
            self._set_error("max_num", num=self.max_num)
            self._is_valid = False
            return None

        is_valid = True

        for form in self._forms:
            form_data = form.validate()
            if not form.validate():
                is_valid = False
                continue

            data.append(form_data)

            if form.updated_fields:
                self.updated = True
            if form._deleted:
                self.updated = True

        self._is_valid = is_valid
        if is_valid:
            return data

    def save(self, parent=None):
        if self._is_valid is None:  # pragma: no cover
            self.validate()
        if self.validate() is False:  # pragma: no cover
            return None

        data = {}
        if self.backref:
            data = {self.backref: parent}

        return list(filter(None, [form.save(**data) for form in self._forms]))

    # Private

    def _set_error(self, name, **kwargs):
        msg = self.error_messages.get(name) or default_error_messages.get(name, "")
        for key, repl in kwargs.items():
            msg = msg.replace("{" + key + "}", str(repl))
        self.error = msg or name


def get_prefixes(prefix, input_data, file_data):
    prefixes = []
    for key in input_data:
        if SEP not in key:
            continue
        prefix, field_name = key.rsplit(SEP, maxsplit=1)
        if prefix not in prefixes:
            prefixes.append(prefix)
    return prefixes

import pytest

import hyperform as f
from hyperform.constants import SEP, NEW, ID, DELETED


class MyModel(object):
    def __init__(self, **kwargs):
        kwargs.setdefault("deleted", False)
        for key, value in kwargs.items():
            setattr(self, key, value)


class ORMForm(f.Form):
    _model = MyModel

    def create_object(self, data):
        return self._model(**data)

    def delete_object(self):
        self._object.deleted = True


def test_load_data_object():
    class WrapperObject(object):
        def __init__(self):
            self.items = [
                MyModel(id=1, name="a"),
                MyModel(id=2, name="b"),
                MyModel(id=3, name="c"),
            ]

    class SubForm(f.Form):
        name = f.Text()

    class WrapperForm(f.Form):
        items = f.FormSet(SubForm)

    input_data = {}
    obj = WrapperObject()
    form = WrapperForm(input_data, obj)

    assert len(form.items) == 3
    assert form.items[0].name.value == "a"
    assert form.items[-1].name.value == "c"
    assert form.validate()


def test_assert_ids():
    class WrapperObject(object):
        def __init__(self):
            self.items = [
                MyModel(name="a"),
                MyModel(name="b"),
            ]

    class SubForm(f.Form):
        name = f.Text()

    class WrapperForm(f.Form):
        items = f.FormSet(SubForm)

    input_data = {}
    obj = WrapperObject()

    with pytest.raises(AssertionError):
        WrapperForm(input_data, obj)


def test_save_without_model():
    class WrapperObject(object):
        def __init__(self):
            self.items = [
                MyModel(id=124, name="a"),
                MyModel(id=125, name="b"),
            ]

    class SubForm(f.Form):
        name = f.Text()

    class WrapperForm(f.Form):
        items = f.FormSet(SubForm)

    input_data = {
        f"items{SEP}124{SEP}name": "name 1",
        f"items{SEP}125{SEP}name": "name 2",
        f"items{SEP}{NEW}1{SEP}name": "name 3",
    }
    obj = WrapperObject()
    form = WrapperForm(input_data, obj)

    assert form.validate()
    assert form.save() == {
        "items": [
            {ID: 124, "name": "name 1"},
            {ID: 125, "name": "name 2"},
            {"name": "name 3"},
        ]
    }


def test_not_save_if_invalid():
    class WrapperObject(object):
        def __init__(self):
            self.items = [
                MyModel(id=124, name="a"),
                MyModel(id=125, name="b"),
            ]

    class SubForm(f.Form):
        name = f.Text(required=True)

    class WrapperForm(f.Form):
        items = f.FormSet(SubForm)

    input_data = {}
    obj = WrapperObject()
    form = WrapperForm(input_data, obj)

    assert form.save() is None


def test_save_with_model():
    class WrapperObject(object):
        def __init__(self):
            self.items = [
                MyModel(id=124, name="a"),
                MyModel(id=125, name="b"),
            ]

    class SubForm(ORMForm):
        name = f.Text()

    class WrapperForm(f.Form):
        _model = WrapperObject

        items = f.FormSet(SubForm)

    input_data = {
        f"items{SEP}124{SEP}name": "name 1",
        f"items{SEP}125{SEP}name": "name 2",
        f"items{SEP}{NEW}1{SEP}name": "name 3",
    }
    obj = WrapperObject()
    form = WrapperForm(input_data, obj)

    assert form.validate()
    assert obj == form.save()
    assert len(obj.items) == 3
    assert obj.items[0].name == "name 1"
    assert obj.items[1].name == "name 2"
    assert obj.items[2].name == "name 3"


def test_save_delete():
    obj1 = MyModel(id=124, name="a")
    obj2 = MyModel(id=125, name="b")

    class WrapperObject(object):
        def __init__(self):
            self.items = [obj1, obj2]

    class SubForm(ORMForm):
        name = f.Text()

    class WrapperForm(f.Form):
        _model = WrapperObject

        items = f.FormSet(SubForm)

    input_data = {
        f"items{SEP}124{SEP}name": "name 1",
        f"items{SEP}125{SEP}{DELETED}": "1",
        f"items{SEP}{NEW}1{SEP}name": "name 3",
    }
    obj = WrapperObject()
    form = WrapperForm(input_data, obj)
    form.save()

    assert len(obj.items) == 2
    assert obj.items[0].name == "name 1"
    assert obj.items[1].name == "name 3"

    assert obj2.deleted


def test_save_cant_delete():
    obj1 = MyModel(id=124, name="a")
    obj2 = MyModel(id=125, name="b")

    class WrapperObject(object):
        def __init__(self):
            self.items = [obj1, obj2]

    class SubForm(ORMForm):
        name = f.Text()

    class WrapperForm(f.Form):
        _model = WrapperObject

        items = f.FormSet(SubForm, can_delete=False)

    input_data = {
        f"items{SEP}124{SEP}name": "name 1",
        f"items{SEP}125{SEP}{DELETED}": "1",
        f"items{SEP}{NEW}1{SEP}name": "name 3",
    }
    obj = WrapperObject()
    form = WrapperForm(input_data, obj)
    form.save()

    assert len(obj.items) == 3
    assert obj.items[0].name == "name 1"
    assert obj.items[1].name is None
    assert obj.items[2].name == "name 3"

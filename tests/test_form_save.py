import proper_form as f
from proper_form.constants import DELETED, ID


class MyModel(object):
    def __init__(self, **kwargs):
        kwargs.setdefault("deleted", False)
        for key, value in kwargs.items():
            setattr(self, key, value)


class MyForm(f.Form):
    _model = MyModel

    a = f.Text()
    b = f.Integer()

    def create_object(self, data):
        return self._model(**data)

    def delete_object(self, obj):
        obj.deleted = True


def test_save_and_create():
    input_data = {"a": "lorem ipsum", "b": "5"}
    form = MyForm(input_data)
    obj = form.save()

    assert isinstance(obj, MyModel)
    assert obj.a == "lorem ipsum"
    assert obj.b == 5


def test_save_and_update():
    input_data = {"a": "lorem ipsum", "b": "5"}
    object_data = MyModel(id=42, a="old value", b=0)
    form = MyForm(input_data, object_data)
    obj = form.save()

    assert isinstance(obj, MyModel)
    assert obj.id == 42
    assert obj.a == "lorem ipsum"
    assert obj.b == 5


def test_save_when_invalid():
    input_data = {"b": "NOT AN INTEGER"}
    form = MyForm(input_data)
    assert form.save() is None


def test_cant_delete_wont_delete():
    input_data = {"a": "lorem ipsum", "b": "5", DELETED: "1"}
    myobj = MyModel(id=42, a="old value", b=0)
    form = MyForm(input_data, myobj)
    obj = form.save()

    assert obj == myobj
    assert obj.a == "lorem ipsum"
    assert obj.b == 5
    assert obj.deleted is False


def test_puff():
    input_data = {"a": "lorem ipsum", "b": "5", DELETED: "1"}
    myobj = MyModel(id=42, a="old value", b=0)
    form = MyForm(input_data, myobj)
    result = form.save(can_delete=True)

    assert result is None
    assert myobj.deleted


def test_no_model_no_created_object():
    class MySimpleForm(MyForm):
        _model = None

    input_data = {"a": "lorem ipsum", "b": "5"}
    form = MySimpleForm(input_data)
    obj = form.save()

    assert obj == {"a": "lorem ipsum", "b": 5}


def test_no_model_no_updated_object():
    class MySimpleForm(MyForm):
        _model = None

    input_data = {"a": "lorem ipsum", "b": "5"}
    myobj = MyModel(id=42, a="old value", b=0)
    form = MySimpleForm(input_data, myobj)
    obj = form.save()

    assert obj == {ID: 42, "a": "lorem ipsum", "b": 5}


def test_no_model_no_deleted_object():
    class MySimpleForm(MyForm):
        _model = None

    input_data = {"a": "lorem ipsum", "b": "5", DELETED: "1"}
    myobj = MyModel(id=42, a="old value", b=0)
    form = MySimpleForm(input_data, myobj)
    obj = form.save(can_delete=True)

    assert obj == {ID: 42, DELETED: True, "a": "lorem ipsum", "b": 5}

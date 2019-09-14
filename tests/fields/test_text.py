from proper_form.fields import Text


def test_clean_called():
    def clean(value):
        return value + "...cleaned"

    field = Text(clean=clean)
    field.input_values = ["value"]
    assert field.validate() == "value...cleaned"


def test_not_required_empty():
    field = Text()
    field.input_values = []
    assert field.validate() is None
    assert field.error is None


def test_not_required_blank():
    field = Text()
    field.input_values = [""]
    assert field.validate() == ""
    assert field.error is None


def test_not_required_empty_collection():
    field = Text(collection=True)
    field.input_values = []
    assert field.validate() is None
    assert field.error is None


def test_not_required_blank_collection():
    field = Text(collection=True)
    field.input_values = [""]
    assert field.validate() == ""
    assert field.error is None


def test_required_empty():
    field = Text(required=True)
    field.input_values = []
    assert field.validate() is None
    assert field.error == "This field is required."


def test_required_blank():
    field = Text(required=True)
    field.input_values == [""]
    assert field.validate() is None
    assert field.error == "This field is required."


def test_required_custom_error_message():
    field = Text(required=True, error_messages={"required": "Show me the value!"})
    field.input_values = []
    assert field.validate() is None
    assert field.error == "Show me the value!"


def test_single():
    field = Text()
    field.input_values = ["a", "b", "c"]
    assert field.validate() == "a"


def test_multiple():
    field = Text(multiple=True)
    field.input_values = ["a", "b", "c"]
    assert field.validate() == ["a", "b", "c"]


def test_collection():
    field = Text(collection=True)
    field.input_values = ["a,b,c"]
    assert field.validate() == "a,b,c"


def test_collection_sep():
    field = Text(sep="|")
    field.input_values = ["a|b|c"]
    assert field.validate() == "a|b|c"


def test_min_num_multiple():
    field = Text(multiple=True, min_num=2)
    field.input_values = ["a", "b", "c"]
    assert field.validate() == ["a", "b", "c"]
    assert field.error is None

    field = Text(multiple=True, min_num=4)
    field.input_values = ["a", "b", "c"]
    assert field.validate() is None
    assert field.error == "You need at least 4 values."


def test_min_num_collection():
    field = Text(collection=True, min_num=2)
    field.input_values = ["a,b,c"]
    assert field.validate() == "a,b,c"
    assert field.error is None

    field = Text(collection=True, min_num=4)
    field.input_values = ["a,b,c"]
    assert field.validate() is None
    assert field.error == "You need at least 4 values."


def test_min_num_custom_error_message():
    field = Text(multiple=True, min_num=4, error_messages={"min_num": "Not enough"})
    field.input_values = ["a", "b", "c"]
    assert field.validate() is None
    assert field.error == "Not enough"


def test_max_num_multiple():
    field = Text(multiple=True, max_num=4)
    field.input_values = ["a", "b", "c"]
    assert field.validate() == ["a", "b", "c"]
    assert field.error is None

    field = Text(multiple=True, max_num=2)
    field.input_values = ["a", "b", "c"]
    assert field.validate() is None
    assert field.error == "You can have at most 2 values."


def test_max_num_collection():
    field = Text(collection=True, max_num=4)
    field.input_values = ["a,b,c"]
    assert field.validate() == "a,b,c"
    assert field.error is None

    field = Text(collection=True, max_num=2)
    field.input_values = ["a,b,c"]
    assert field.validate() is None
    assert field.error == "You can have at most 2 values."


def test_max_num_custom_error_message():
    field = Text(multiple=True, max_num=2, error_messages={"max_num": "Too much"})
    field.input_values = ["a", "b", "c"]
    assert field.validate() is None
    assert field.error == "Too much"


class VTrue(object):
    called = False

    def __init__(self, message):
        self.message = message

    def __call__(self, values):
        self.called = True
        return True


class VFalse(object):
    called = False

    def __init__(self, message):
        self.message = message

    def __call__(self, values):
        self.called = True
        return False, self.message


def test_validators_called():
    v1 = VTrue(message="v1")
    v2 = VTrue(message="v2")
    v3 = VFalse(message="v3")
    v4 = VTrue(message="v4")

    field = Text(v1, v2, v3, v4)
    field.input_values = ["value"]
    assert field.validate() is None
    assert field.error == "v3"

    assert v1.called
    assert v2.called
    assert v3.called
    assert not v4.called

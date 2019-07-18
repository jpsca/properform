from unittest.mock import Mock

from proper_form.fields import Text


def test_prepare_called():
    def prepare(values):
        return ["prepared..." + values[0]]

    field = Text(prepare=prepare)
    assert field.validate(["value"]) == "prepared...value"


def test_clean_called():
    def clean(value):
        return value + "...cleaned"

    field = Text(clean=clean)
    assert field.validate(["value"]) == "value...cleaned"


def test_not_required():
    field = Text()
    assert field.validate([]) is None
    assert field.error is None


def test_required():
    field = Text(required=True)
    assert field.validate([]) is None
    assert field.error == "This field is required."


def test_required_custom_error_message():
    field = Text(required=True, error_messages={"required": "Show me the value!"})
    assert field.validate([]) is None
    assert field.error == "Show me the value!"


def test_single():
    field = Text()
    assert field.validate(["a", "b", "c"]) == "a"


def test_multiple():
    field = Text(multiple=True)
    assert field.validate(["a", "b", "c"]) == ["a", "b", "c"]


def test_collection():
    field = Text(collection=True)
    assert field.validate(["a,b,c"]) == "a,b,c"


def test_collection_sep():
    field = Text(sep="|")
    assert field.validate(["a|b|c"]) == "a|b|c"


def test_min_num_values_multiple():
    field = Text(multiple=True, min_num_values=2)
    assert field.validate(["a", "b", "c"]) == ["a", "b", "c"]
    assert field.error is None

    field = Text(multiple=True, min_num_values=4)
    assert field.validate(["a", "b", "c"]) is None
    assert field.error == "You need at least 4 values."


def test_min_num_values_collection():
    field = Text(collection=True, min_num_values=2)
    assert field.validate(["a,b,c"]) == "a,b,c"
    assert field.error is None

    field = Text(collection=True, min_num_values=4)
    assert field.validate(["a,b,c"]) is None
    assert field.error == "You need at least 4 values."


def test_min_num_values_custom_error_message():
    field = Text(multiple=True, min_num_values=4, error_messages={"min_num_values": "Not enough"})
    assert field.validate(["a", "b", "c"]) is None
    assert field.error == "Not enough"


def test_max_num_values_multiple():
    field = Text(multiple=True, max_num_values=4)
    assert field.validate(["a", "b", "c"]) == ["a", "b", "c"]
    assert field.error is None

    field = Text(multiple=True, max_num_values=2)
    assert field.validate(["a", "b", "c"]) is None
    assert field.error == "You can have at most 2 values."


def test_max_num_values_collection():
    field = Text(collection=True, max_num_values=4)
    assert field.validate(["a,b,c"]) == "a,b,c"
    assert field.error is None

    field = Text(collection=True, max_num_values=2)
    assert field.validate(["a,b,c"]) is None
    assert field.error == "You can have at most 2 values."


def test_max_num_values_custom_error_message():
    field = Text(multiple=True, max_num_values=2, error_messages={"max_num_values": "Too much"})
    assert field.validate(["a", "b", "c"]) is None
    assert field.error == "Too much"

import hyperform.fields as f


def test_text_as_checkbox():
    field = f.Text(name="name")
    assert field.as_checkbox() == \
        '<input name="name" type="checkbox">'


def test_text_as_checkbox_with_label():
    field = f.Text(name="name")
    assert field.as_checkbox(label="I have read the TOS") == \
        '<label class="checkbox"><input name="name" type="checkbox"> I have read the TOS</label>'


def test_text_as_checkbox_checked():
    field = f.Text(name="name")
    field.input_values = ["hello"]
    assert field.as_checkbox() == \
        '<input name="name" type="checkbox" checked>'


def test_boolean_as_checkbox():
    field = f.Boolean(name="name")
    assert field.as_checkbox() == \
        '<input name="name" type="checkbox">'


def test_boolean_as_checkbox_checked():
    field = f.Boolean(name="name")
    field.object_value = True
    assert field.as_checkbox() == \
        '<input name="name" type="checkbox" checked>'


def test_boolean_as_checkbox_force_checked():
    field = f.Boolean(name="name")
    assert field.as_checkbox(checked=True) == \
        '<input name="name" type="checkbox" checked>'


def test_boolean_as_checkbox_custom_value():
    field = f.Boolean(name="name")
    assert field.as_checkbox(value="newsletter") == \
        '<input name="name" type="checkbox" value="newsletter">'


def test_boolean_as_checkbox_custom_value_checked():
    field = f.Boolean(name="name")
    field.input_values = ["newsletter"]
    assert field.as_checkbox(value="newsletter") == \
        '<input name="name" type="checkbox" value="newsletter" checked>'


def test_boolean_as_checkbox_custom_str_value_checked():
    field = f.Boolean(name="name")
    field.input_values = [5]
    assert field.as_checkbox(value="5") == \
        '<input name="name" type="checkbox" value="5" checked>'


def test_boolean_as_checkbox_custom_str_reverse_value_checked():
    field = f.Boolean(name="name")
    field.input_values = ["5"]
    assert field.as_checkbox(value=5) == \
        '<input name="name" type="checkbox" value="5" checked>'


def test_boolean_as_checkbox_custom_values_checked():
    field = f.Boolean(name="name", multiple=True)
    field.input_values = ["alerts", "newsletter", "replies"]
    assert field.as_checkbox(value="newsletter") == \
        '<input name="name" type="checkbox" value="newsletter" checked>'


def test_boolean_as_checkbox_custom_value_unchecked():
    field = f.Boolean(name="name")
    field.input_values = ["newsletter"]
    assert field.as_checkbox(value="direct") == \
        '<input name="name" type="checkbox" value="direct">'


def test_boolean_as_checkbox_custom_values_unchecked():
    field = f.Boolean(name="name", multiple=True)
    field.input_values = ["alerts", "newsletter", "replies"]
    assert field.as_checkbox(value="direct") == \
        '<input name="name" type="checkbox" value="direct">'


def test_boolean_as_checkbox_custom_value_object_unchecked():
    field = f.Boolean(name="name")
    field.object_value = True
    assert field.as_checkbox(value="newsletter") == \
        '<input name="name" type="checkbox" value="newsletter">'

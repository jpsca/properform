import proper_form.fields as f


def test_text_as_radio():
    field = f.Text(name="name")
    assert field.as_radio() == \
        '<input name="name" type="radio">'


def test_text_as_radio_checked():
    field = f.Text(name="name")
    field.input_values = ["hello"]
    assert field.as_radio() == \
        '<input name="name" type="radio" checked>'


def test_boolean_as_radio():
    field = f.Boolean(name="name")
    assert field.as_radio() == \
        '<input name="name" type="radio">'


def test_boolean_as_radio_checked():
    field = f.Boolean(name="name")
    field.object_value = True
    assert field.as_radio() == \
        '<input name="name" type="radio" checked>'


def test_boolean_as_radio_force_checked():
    field = f.Boolean(name="name")
    assert field.as_radio(checked=True) == \
        '<input name="name" type="radio" checked>'


def test_boolean_as_radio_custom_value():
    field = f.Boolean(name="name")
    assert field.as_radio(value="newsletter") == \
        '<input name="name" type="radio" value="newsletter">'


def test_boolean_as_radio_custom_value_checked():
    field = f.Boolean(name="name")
    field.input_values = ["newsletter"]
    assert field.as_radio(value="newsletter") == \
        '<input name="name" type="radio" value="newsletter" checked>'


def test_boolean_as_radio_custom_values_checked():
    field = f.Boolean(name="name", multiple=True)
    field.input_values = ["alerts", "newsletter", "replies"]
    assert field.as_radio(value="newsletter") == \
        '<input name="name" type="radio" value="newsletter" checked>'


def test_boolean_as_radio_custom_value_unchecked():
    field = f.Boolean(name="name")
    field.input_values = ["newsletter"]
    assert field.as_radio(value="direct") == \
        '<input name="name" type="radio" value="direct">'


def test_boolean_as_radio_custom_values_unchecked():
    field = f.Boolean(name="name", multiple=True)
    field.input_values = ["alerts", "newsletter", "replies"]
    assert field.as_radio(value="direct") == \
        '<input name="name" type="radio" value="direct">'


def test_boolean_as_radio_custom_value_object_unchecked():
    field = f.Boolean(name="name")
    field.object_value = True
    assert field.as_radio(value="newsletter") == \
        '<input name="name" type="radio" value="newsletter">'

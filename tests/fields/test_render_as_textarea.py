import proper_form.fields as f


def test_text_as_textarea():
    field = f.Text(name="name")
    field.input_values = ["hello"]
    expected = '<textarea name="name">hello</textarea>'
    assert field.as_textarea() == expected


def test_text_as_textarea_no_value():
    field = f.Text(name="name")
    expected = '<textarea name="name"></textarea>'
    assert field.as_textarea() == expected


def test_text_as_textarea_with_label():
    field = f.Text(name="name")
    expected = (
        '<label for="name">Hello World</label>\n'
        '<textarea id="name" name="name"></textarea>'
    )
    assert field.as_textarea(label="Hello World") == expected


def test_text_as_textarea_attributes():
    field = f.Text(name="name")
    expected = '<textarea data-id="2" name="name" extra></textarea>'
    assert field.as_textarea(data_id=2, extra=True) == expected


def test_text_as_textarea_required():
    field = f.Text(name="name", required=True)
    expected = '<textarea name="name" required></textarea>'
    assert field.as_textarea() == expected

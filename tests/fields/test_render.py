import hyperform.fields as f


def test_render_attrs():
    field = f.Text()
    attrs = {
        "id": "text1",
        "classes": "myclass",
        "data_id": 1,
        "checked": True,
        "ignore": False,
    }
    assert (
        str(field.render_attrs(**attrs))
        == 'class="myclass" data-id="1" id="text1" checked'
    )


def test_render_attrs_empty():
    field = f.Text()
    assert str(field.render_attrs()) == ""


def test_render_attrs_bad():
    field = f.Text()
    assert (
        str(field.render_attrs(myattr="a'b\"><script>bad();</script>"))
        == 'myattr="a\'b&quot;&gt;&lt;script&gt;bad();&lt;/script&gt;"'
    )


def test_object_value():
    field = f.Text(prepare=lambda x: [str(x * 2)])
    field.object_value = 2
    assert field.values == ["4"]
    assert field.value == "4"


def test_input_values():
    field = f.Text()
    field.input_values = ["hello"]
    assert field.values == ["hello"]
    assert field.value == "hello"


def test_input_value_over_object_value():
    field = f.Text()
    field.input_values = ["foo"]
    field.object_value = "bar"
    assert field.values == ["foo"]
    assert field.value == "foo"


def test_render_error():
    field = f.Text(required=True)
    assert str(field.render_error()) == ""

    field.validate()
    error = "This field is required."

    assert str(field.render_error()) == f'<div class="error">{error}</div>'
    assert str(field.render_error("p")) == f'<p class="error">{error}</p>'
    assert (
        str(field.render_error(classes="errorMessage"))
        == f'<div class="errorMessage">{error}</div>'
    )

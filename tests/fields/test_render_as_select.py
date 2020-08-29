import hyperform.fields as f


def test_render_as_select_tag():
    field = f.Integer()
    assert field.as_select_tag() == \
        '<select name="">'


def test_render_as_select_tag_properties():
    field = f.Integer(required=True, multiple=True)
    assert field.as_select_tag() == \
        '<select name="" multiple required>'


def test_render_as_select_tag_attrs():
    field = f.Integer()
    assert field.as_select_tag(data_format="local", selectize=True) == \
        '<select data-format="local" name="" selectize>'


def test_render_as_select_tag_with_label():
    field = f.Integer(name="name")
    assert field.as_select_tag(label="Choose one") == \
        '<label for="name">Choose one</label>\n<select name="name">'


def test_text_render_as_select():
    field = f.Integer(name="meh")
    items = [
        ("lorem", 1),
        ("ipsum", "2"),
        ("sit amet", "3"),
    ]
    result = field.as_select(items)
    expected = (
        '<select name="meh">\n'
        '<option value="1">lorem</option>\n'
        '<option value="2">ipsum</option>\n'
        '<option value="3">sit amet</option>\n'
        "</select>"
    )
    assert result == expected


def test_text_render_as_select_with_attrs():
    field = f.Integer(name="meh")
    items = [
        ("lorem", 1, {"data_id": "1"}),
        ("ipsum", "2", {"data_id": "2"}),
        ("sit amet", "3", {"data_id": "3"}),
    ]
    result = field.as_select(items)
    expected = (
        '<select name="meh">\n'
        '<option data-id="1" value="1">lorem</option>\n'
        '<option data-id="2" value="2">ipsum</option>\n'
        '<option data-id="3" value="3">sit amet</option>\n'
        "</select>"
    )
    assert result == expected


def test_text_render_as_select_input_selected():
    field = f.Integer(name="meh")
    field.input_values = ["2"]
    items = [
        ("lorem", 1),
        ("ipsum", "2"),
        ("sit amet", "3"),
    ]
    result = field.as_select(items)
    expected = (
        '<select name="meh">\n'
        '<option value="1">lorem</option>\n'
        '<option value="2" selected>ipsum</option>\n'
        '<option value="3">sit amet</option>\n'
        "</select>"
    )
    assert result == expected


def test_text_render_as_select_input_selected_typecasted():
    field = f.Integer(name="meh")
    field.input_values = [2]
    items = [
        ("lorem", 1),
        ("ipsum", "2"),
        ("sit amet", "3"),
    ]
    result = field.as_select(items)
    expected = (
        '<select name="meh">\n'
        '<option value="1">lorem</option>\n'
        '<option value="2" selected>ipsum</option>\n'
        '<option value="3">sit amet</option>\n'
        "</select>"
    )
    assert result == expected


def test_text_render_as_select_multiple():
    field = f.Integer(name="meh", multiple=True)
    field.input_values = [1, 4]
    items = [
        ("lorem", 1),
        ("ipsum", "2"),
        ("sit amet", "3"),
        ("dolum", "4"),
    ]
    result = field.as_select(items)
    expected = (
        '<select name="meh" multiple>\n'
        '<option value="1" selected>lorem</option>\n'
        '<option value="2">ipsum</option>\n'
        '<option value="3">sit amet</option>\n'
        '<option value="4" selected>dolum</option>\n'
        "</select>"
    )
    assert result == expected


def test_text_render_as_select_with_optgroups():
    field = f.Text(name="city")
    items = [
        ("America", [
            ("New York", 1),
            ("Boston", 2),
            ("Toronto", 3),
            ("Lima", 4),
        ]),
        ("Europe", [
            ("Rome", 5),
            ("Madrid", 6),
            ("Paris", 7),
            ("London", 8),
        ]),
    ]
    result = field.as_select(items)
    expected = (
        '<select name="city">\n'
        '<optgroup label="America">\n'
        '<option value="1">New York</option>\n'
        '<option value="2">Boston</option>\n'
        '<option value="3">Toronto</option>\n'
        '<option value="4">Lima</option>\n'
        '</optgroup>\n'
        '<optgroup label="Europe">\n'
        '<option value="5">Rome</option>\n'
        '<option value="6">Madrid</option>\n'
        '<option value="7">Paris</option>\n'
        '<option value="8">London</option>\n'
        '</optgroup>\n'
        "</select>"
    )
    assert result == expected

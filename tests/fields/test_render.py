from proper_form.fields.render import get_html_attrs


def test_html_attrs():
    attrs = {
        "id": "text1",
        "className": "myclass",
        "data_id": 1,
        "checked": True,
        "ignore": False,
    }
    expected = 'class="myclass" data-id="1" id="text1" checked'
    result = get_html_attrs(attrs)
    assert result == expected


def test_html_attrs_empty():
    assert get_html_attrs() == ""


def test_html_attrs_bad():
    result = get_html_attrs({"myattr": "a'b\"><script>bad();</script>"})
    expected = 'myattr="a\'b&quot;&gt;&lt;script&gt;bad();&lt;/script&gt;"'
    assert result == expected

import re
from xml.sax.saxutils import quoteattr

from markupsafe import Markup, escape_silent

from ..types import type_boolean


rx_spaces = re.compile(r"\s+")


def get_html_attrs(attrs=None):
    """Generate HTML attributes from the provided attributes.

    - To provide consistent output, the attributes and properties are sorted by name
    and rendered liek this: `<sorted attributes> + <sorted properties>`.
    - "className" can be used intead of "class", to avoid clashes with the
    reserved word.
    - Also, all underscores are translated to regular dashes.
    - Set properties with a `True` value.

    >>> get_html_attrs({
    ...     "id": "text1",
    ...     "className": "myclass",
    ...     "data_id": 1,
    ...     "checked": True,
    ... })
    'class="myclass" data-id="1" id="text1" checked'

    """
    attrs = attrs or {}
    attrs_list = []
    props_list = []

    classes = (attrs.pop("class", "") + " " + attrs.pop("className", "")).strip()
    if classes:
        attrs["class"] = " ".join(rx_spaces.split(classes))

    for key, value in attrs.items():
        key = key.replace("_", "-")
        if value is True:
            props_list.append(key)
        elif value not in (False, None):
            value = quoteattr(str(value))
            attrs_list.append("{}={}".format(key, value))

    attrs_list.sort()
    props_list.sort()
    attrs_list.extend(props_list)
    return " ".join(attrs_list)


def in_(value, values):
    """Test if the value is in a list of values, or if the value as string is, or
    if the value is one of the values as strings.
    """
    ext_values = values + [str(val) for val in values]
    return value in ext_values or str(value) in ext_values


class RenderedField(object):

    @property
    def auto_id(self):
        """Generates a unique value for using the id attribute of the rendered field.
        """
        return "{}_{}".format(self.prefix, self.name)

    def render_attrs(self, **attrs):
        html = get_html_attrs(attrs)
        return Markup(html)

    def as_input(self, *, label=None, **attrs):
        """Renders the field as a `<input type="text">` element, although the type
        can be changed.

        kwargs (dict):
            Named parameters used to generate the HTML attributes.
            It follows the same rules as `get_html_attrs`

        """
        attrs.setdefault("name", self.name)
        attrs.setdefault("required", self.required)
        attrs.setdefault("type", self.input_type)
        attrs.setdefault("value", self.value or "")
        if label:
            attrs.setdefault("id", self.auto_id)
        html = "<input {}>".format(get_html_attrs(attrs))
        if label:
            label = escape_silent(str(label))
            html = '<label for="{}">{}</label>\n{}'.format(attrs["id"], label, html)
        return Markup(html)

    def as_textarea(self, *, label=None, **attrs):
        """Renders the field as a `<textarea>` tag.

        kwargs (dict):
            Named parameters used to generate the HTML attributes.
            It follows the same rules as `get_html_attrs`

        """
        attrs.setdefault("name", self.name)
        attrs.setdefault("required", self.required)
        if label:
            attrs.setdefault("id", self.auto_id)
        html_attrs = get_html_attrs(attrs)
        value = attrs.pop("value", None) or self.value or ""
        html = "<textarea {}>{}</textarea>".format(html_attrs, value)
        if label:
            label = escape_silent(str(label))
            html = '<label for="{}">{}</label>\n{}'.format(attrs["id"], label, html)
        return Markup(html)

    def as_checkbox(self, *, label=None, **attrs):
        """Renders the field as a `<input type="checkbox">` tag.

        kwargs (dict):
            Named parameters used to generate the HTML attributes.
            It follows the same rules as `get_html_attrs`

        """
        attrs.setdefault("name", self.name)
        attrs["type"] = "checkbox"
        attrs.setdefault("required", self.required)

        value = attrs.get("value")
        if value is not None:
            attrs.setdefault("checked", in_(value, self.values))
        else:
            attrs.setdefault("checked", type_boolean(self.value))

        html = "<input {}>".format(get_html_attrs(attrs))

        if label:
            label = escape_silent(str(label))
            html = '<label class="checkbox">{} {}</label>'.format(html, label)

        return Markup(html)

    def as_radio(self, *, label=None, **attrs):
        """Renders the field as a `<input type="radio">` tag.

        kwargs (dict):
            Named parameters used to generate the HTML attributes.
            It follows the same rules as `get_html_attrs`

        """
        attrs.setdefault("name", self.name)
        attrs["type"] = "radio"
        attrs.setdefault("required", self.required)

        value = attrs.get("value")
        if value is not None:
            attrs.setdefault("checked", in_(value, self.values))
        else:
            attrs.setdefault("checked", type_boolean(self.value))

        html = "<input {}>".format(get_html_attrs(attrs))

        if label:
            label = escape_silent(str(label))
            html = '<label class="radio">{} {}</label>'.format(html, label)

        return Markup(html)

    def as_select_tag(self, *, label=None, **attrs):
        """Renders *just* the opening `<select>` tag for a field, not any options
        nor the closing "</select>".

        This is intended to be used with `<option>` tags writted by hand or genereated
        by other means.

        kwargs (dict):
            Named parameters used to generate the HTML attributes.
            It follows the same rules as `get_html_attrs`

        """
        attrs.setdefault("name", self.name)
        attrs.setdefault("required", self.required)
        attrs.setdefault("multiple", self.multiple)
        if label:
            attrs.setdefault("id", self.auto_id)
        html = "<select {}>".format(get_html_attrs(attrs))

        if label:
            label = escape_silent(str(label))
            html = '<label for="{}">{}</label>\n{}'.format(attrs["id"], label, html)

        return Markup(html)

    def as_select(self, items, *, label=None, **attrs):
        """Renders the field as a `<select>` tag.

        items (list):
            ...

        kwargs (dict):
            Named parameters used to generate the HTML attributes.
            It follows the same rules as `get_html_attrs`

        """

        html = [str(self.as_select_tag(label=label, **attrs))]

        for item in items:
            label, value = item[:2]
            if isinstance(value, (list, tuple)):
                tags = self.render_optgroup(label, value, self.values)
            else:
                tags = self.render_option(item, self.values)
            html.append(str(tags))

        html.append("</select>")
        return Markup("\n".join(html))

    def render_optgroup(self, label, items, values=None, **attrs):
        """Renders an <optgroup> tag with <options>.

        label (str):
            ...

        items (list):
            ...

        values (any|list|None):
            A value or a list of "selected" values.

        kwargs (dict):
            Named parameters used to generate the HTML attributes.
            It follows the same rules as `get_html_attrs`

        """
        label = escape_silent(str(label))
        html = ['<optgroup label="{}">'.format(label)]

        for item in items:
            tag = self.render_option(item, values, **attrs)
            html.append(str(tag))

        html.append("</optgroup>")
        return Markup("\n".join(html))

    def render_option(self, item, values=None, **attrs):
        """Renders an <option> tag

        item (tuple|list):
            A (value, label) or (value, label, {attrs}) tuple.

        values (any|list|None):
            A value or a list of "selected" values.

        kwargs (dict):
            Named parameters used to generate the HTML attributes.
            It follows the same rules as `get_html_attrs`

        """
        values = values or []
        assert isinstance(values, (list, tuple))

        label, value = item[:2]
        if len(item) > 2:
            attrs.update(item[2])

        attrs.setdefault("value", value)
        attrs["selected"] = in_(value, values)
        label = escape_silent(str(label))
        tag = "<option {}>{}</option>".format(get_html_attrs(attrs), label)
        return Markup(tag)

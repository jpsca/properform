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


# "<label {}>{}</label>"


class RenderedField(object):

    @property
    def values(self):
        if self.input_values is not None:
            return self.input_values or [""]
        if self.object_value is not None:
            return self.prepare(self.object_value) or [""]
        return [""]

    @property
    def value(self):
        return self.values[0] if self.values else None

    def auto_id(self):
        """Generates a unique value for using the id attribute of the rendered field.
        """
        return "{}_{}_".format(self.prefix, self.name)

    def as_input(self, *, label=None, **attrs):
        """Renders the field as a `<input type="text">` element, although the type
        can be changed.

        kwargs (dict):
            Named parameters used to generate the HTML attributes.
            It follows the same rules as `get_html_attrs`

        """
        attrs.setdefault("name", self.name)
        attrs.setdefault("required", self.required)
        attrs.setdefault("id", self.auto_id())
        attrs.setdefault("type", self.input_type)
        attrs.setdefault("value", self.value)
        html = "<input {}>".format(get_html_attrs(attrs))
        if label:
            label = escape_silent(str(label))
            html = '<label for="{}">{}</label>/n{}'.format(attrs["id"], label, html)
        return Markup(html)

    def as_textarea(self, *, label=None, **attrs):
        """Renders the field as a `<textarea>` tag.

        kwargs (dict):
            Named parameters used to generate the HTML attributes.
            It follows the same rules as `get_html_attrs`

        """
        attrs.setdefault("name", self.name)
        attrs.setdefault("required", self.required)
        attrs.setdefault("id", self.auto_id())
        html_attrs = get_html_attrs(attrs)
        value = attrs.get("value", self.value)
        html = "<textarea {}>{}</textarea>".format(html_attrs, value)
        if label:
            label = escape_silent(str(label))
            html = '<label for="{}">{}</label>/n{}'.format(attrs["id"], label, html)
        return Markup(html)

    def as_checkbox(self, *, label=None, **attrs):
        """Renders the field as a `<input type="checkbox">` tag.

        kwargs (dict):
            Named parameters used to generate the HTML attributes.
            It follows the same rules as `get_html_attrs`

        """
        attrs.setdefault("name", self.name)
        attrs["type"] = "checkbox"
        if type_boolean(self.value):
            attrs.setdefault("checked", True)
        attrs.setdefault("required", self.required)
        html = "<input {}>".format(get_html_attrs(attrs))
        if label:
            label = escape_silent(str(label))
            html = '<label class="checkbox">{} {}</label>'.format(html, label)
        return Markup(html)

    def as_select_tag(self, **attrs):
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
        tag = "<select {}>".format(get_html_attrs(attrs))
        return Markup(tag)

    def as_select(self, items, *, label=None, **attrs):
        """Renders the field as a `<select>` tag.

        items (list):
            ...

        kwargs (dict):
            Named parameters used to generate the HTML attributes.
            It follows the same rules as `get_html_attrs`

        """
        attrs.setdefault("id", self.auto_id())
        html = [str(self.as_select_tag(**attrs))]

        for item in items:
            if isinstance(item, (list, tuple)):
                if not item:
                    continue
                tags = self.render_optgroup(item[0], item[1:], self.values)
            else:
                tags = self.render_option(item, self.values)
            html.append(str(tags))

        html.append("</select>")
        if label:
            label = escape_silent(str(label))
            html = '<label class="radiobutton">{} {}</label>'.format(html, label)
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
            A (value, label) tuple.

        values (any|list|None):
            A value or a list of "selected" values.

        kwargs (dict):
            Named parameters used to generate the HTML attributes.
            It follows the same rules as `get_html_attrs`

        """
        values = values or []
        if values:
            if not isinstance(values, (list, tuple)):
                values = [values]

        val, label = item[:2]
        attrs.setdefault("value", val)
        attrs["selected"] = val in values or str(val) in values
        label = escape_silent(str(label))
        tag = "<option {}>{}</option>".format(get_html_attrs(attrs), label)
        return Markup(tag)

    def render_radiobutton(self, item, values=None, **attrs):
        values = values or []
        if values:
            if not isinstance(values, (list, tuple)):
                values = [values]

        val, label = item[:2]
        attrs.setdefault("value", val)
        attrs["selected"] = val in values or str(val) in values
        attrs["type"] = "radio"
        label = escape_silent(str(label))
        html = '<label class="radiobutton"><input {}> {}</label>'.format(
            get_html_attrs(attrs), label
        )
        return Markup(html)

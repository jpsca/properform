from markupsafe import Markup, escape_silent

from ..ftypes import type_boolean
from ..utils import get_html_attrs


__all__ = ("FieldRenderable", "get_html_attrs", "in_")


class FieldRenderable(object):

    def render_attrs(self, **attrs):
        html = get_html_attrs(attrs, show_error=self.error)
        return Markup(html)

    def label(self, text, html="", **attrs):
        text = escape_silent(str(text))
        attrs.setdefault("for", self.name)
        html_attrs = get_html_attrs(attrs, show_error=self.error)
        if html:
            html = html + " "
        return "<label {}>{}{}</label>".format(html_attrs, html, text)

    def as_input(self, *, label=None, **attrs):
        """Renders the field as a `<input type="text">` element, although the type
        can be changed.

        attrs (dict):
            Named parameters used to generate the HTML attributes.
            It follows the same rules as `get_html_attrs`

        """
        attrs.setdefault("name", self.name)
        attrs.setdefault("required", self.required)
        attrs.setdefault("type", self.input_type)
        attrs.setdefault("value", self.value or "")
        if label:
            attrs.setdefault("id", self.name)
        html_attrs = get_html_attrs(attrs, show_error=self.error)

        html = "<input {}>".format(html_attrs)
        if label and label != True:
            kwargs = {"for": attrs.get("id")}
            html = self.label(label, **kwargs) + "\n" + html
        return Markup(html)

    def as_textarea(self, *, label=None, **attrs):
        """Renders the field as a `<textarea>` tag.

        attrs (dict):
            Named parameters used to generate the HTML attributes.
            It follows the same rules as `get_html_attrs`

        """
        attrs.setdefault("name", self.name)
        attrs.setdefault("required", self.required)
        if label:
            attrs.setdefault("id", self.name)
        html_attrs = get_html_attrs(attrs, show_error=self.error)

        value = attrs.pop("value", None) or self.value or ""
        html = "<textarea {}>{}</textarea>".format(html_attrs, value)
        if label and label != True:
            kwargs = {"for": attrs.get("id")}
            html = self.label(label, **kwargs) + "\n" + html
        return Markup(html)

    def as_checkbox(self, *, label=None, **attrs):
        """Renders the field as a `<input type="checkbox">` tag.

        attrs (dict):
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
        html_attrs = get_html_attrs(attrs, show_error=self.error)

        html = "<input {}>".format(html_attrs)
        if label and label != True:
            kwargs = {
                "for": attrs.get("id"),
                "classes": attrs.get("classes", "checkbox"),
            }
            html = self.label(label, html=html, **kwargs)

        return Markup(html)

    def as_radio(self, *, label=None, **attrs):
        """Renders the field as a `<input type="radio">` tag.

        attrs (dict):
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
        html_attrs = get_html_attrs(attrs, show_error=self.error)

        html = "<input {}>".format(html_attrs)
        if label and label != True:
            kwargs = {
                "for": attrs.get("id"),
                "classes": attrs.get("classes", "radio"),
            }
            html = self.label(label, html=html, **kwargs)

        return Markup(html)

    def as_select_tag(self, *, label=None, **attrs):
        """Renders *just* the opening `<select>` tag for a field, not any options
        nor the closing "</select>".

        This is intended to be used with `<option>` tags writted by hand or genereated
        by other means.

        attrs (dict):
            Named parameters used to generate the HTML attributes.
            It follows the same rules as `get_html_attrs`

        """
        attrs.setdefault("name", self.name)
        attrs.setdefault("required", self.required)
        attrs.setdefault("multiple", self.multiple)
        if label:
            attrs.setdefault("id", self.name)
        html_attrs = get_html_attrs(attrs, show_error=self.error)

        html = "<select {}>".format(html_attrs)
        if label and label != True:
            kwargs = {"for": attrs.get("id")}
            html = self.label(label, **kwargs) + "\n" + html

        return Markup(html)

    def as_select(self, items, *, label=None, **attrs):
        """Renders the field as a `<select>` tag.

        items (list):
            ...

        attrs (dict):
            Named parameters used to generate the HTML attributes.
            It follows the same rules as `get_html_attrs`

        """

        html = [str(self.as_select_tag(label=label, **attrs))]

        for item in items:
            label, value = item[:2]
            if isinstance(value, (list, tuple)):
                tags = self.render_optgroup(label, value)
            else:
                opattrs = item[2] if len(item) > 2 else {}
                tags = self.render_option(label, value, **opattrs)
            html.append(str(tags))

        html.append("</select>")
        return Markup("\n".join(html))

    def render_optgroup(self, label, items, **attrs):
        """Renders an <optgroup> tag with <options>.

        label (str):
            ...

        items (list):
            ...

        values (any|list|None):
            A value or a list of "selected" values.

        attrs (dict):
            Named parameters used to generate the HTML attributes.
            It follows the same rules as `get_html_attrs`

        """
        attrs["label"] = escape_silent(str(label))
        html_attrs = get_html_attrs(attrs, show_error=self.error)
        html = ['<optgroup {}>'.format(html_attrs)]

        for item in items:
            oplabel, opvalue = item[:2]
            opattrs = item[2] if len(item) > 2 else {}
            tag = self.render_option(oplabel, opvalue, **opattrs)
            html.append(str(tag))

        html.append("</optgroup>")
        return Markup("\n".join(html))

    def render_option(self, label, value=None, **attrs):
        """Renders an <option> tag

        label:
            Text of the option

        value:
            Value for the option (sames as the label by default).

        attrs (dict):
            Named parameters used to generate the HTML attributes.
            It follows the same rules as `get_html_attrs`

        """
        values = self.values or []
        value = label if value is None else value
        attrs.setdefault("value", value)
        attrs["selected"] = in_(value, values)
        label = escape_silent(str(label))
        html_attrs = get_html_attrs(attrs, show_error=self.error)
        tag = "<option {}>{}</option>".format(html_attrs, label)
        return Markup(tag)

    def render_error(self, tag="div", **attrs):
        if not self.error:
            return ""

        attrs.setdefault("classes", "error")
        return Markup("<{tag} {attrs}>{error}</{tag}>".format(
            tag=tag,
            attrs=get_html_attrs(attrs, show_error=False),
            error=self.error,
        ))


def in_(value, values):
    """Test if the value is in a list of values, or if the value as string is, or
    if the value is one of the values as strings.
    """
    ext_values = values + [str(val) for val in values]
    return value in ext_values or str(value) in ext_values

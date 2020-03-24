
# Rendering

Instead of rendering a form with a predefined static markup, wih Proper Form you render its individual fields. For example:

```html+jinja
<form method="post" action="">
  {{ form.render_error() }}
  <div class="col">
    {{ form.myname.as_input(label="Name:") }}
    {{ form.myname.render_error() }}
  </div>
  <div class="col">
    {{ form.myemail.as_input(label="Email:") }}
    {{ form.myemail.render_error() }}
  </div>
</form>
```

that will render to:

```html
<form method="post" action="">
  <div class="col">
    <label for="myname">Name:</label>
    <input id="myname" name="myname" type="text">
  </div>
  <div class="col">
    <label for="myemail">Email:</label>
    <input id="myemail" name="myemail" type="email">
  </div>
</form>
```

As in the example, the usual thing to do is to also to add the rendering code for the field error right below (or at the top) of it. If there is no error nothing will be rendered there anyway.

The form can also have a `form.error` attribute manually set by you.


## Available methods

One of the thing Proper Form does different is that it doesn't tie a field type to a specific HTML tag. You might think an URL field it's always going to be displayed as an `<input>`, but *it doesn't have to*. You could also have URLs as values of checkboxes, radio buttons, or selects.

For that reason, all of these method are available for all fields, no matter its data type.


### About HTML attributes

All of these methods accept any number of `key=value` optional arguments. These'll be included as HTML attributes. Use `classes` instead of `class`.

```python
>>> field.as_input(classes="someclass anotherone", zzz="bar")
'<input class="someclass anotherone" name="field" type="text" zzz="bar">'
```

If you need an attribute with a dash, like `data-id`, use an underscore `data_id=123`. For properties (attributes without values) just use `True` as its value.

```python
>>> field.as_input(data_id=123, data_target=True)
'<input data_id="123" name="field" type="text" data-target>'
```


### as_input( )

```python
field.as_input(label=None, **attrs)
```

Renders the field as a `<input type="text">` element, although the type can be overwritten.

If you use a `label` argument, a `<label>` will be added before the input, and also an `id` attribute to connect both (that can also be overwritten).

Examples:

```python
>>> form.url.as_input()
'<input name="url" type="url">'

# If the field has `required=True'
>>> form.url.as_input()
'<input name="url" type="url" required>'

>>> form.url.as_input(type="text", classes="form-control")
'<input class="form-control" name="url" type="text">'

>>> form.url.as_input(label="Webpage:")
'<label for="url">Webpage:</label>\n<input id="url" name="url" type="url">'

>>> form.url.as_input(label="Webpage:", id="12345")
'<label for="12345">Webpage:</label>\n<input id="12345" name="url" type="url">'
```


### as_textarea( )

```python
field.as_textarea(label=None, **attrs)
```

Renders the field as a `<textarea>` element.

If you use a `label` argument, a `<label>` will be added before the input, and also an `id` attribute to connect both (that can also be overwritten).

Examples:

```python
>>> form.bio.as_textarea()
'<textarea name="bio"></textarea>'

>>> form.bio.as_textarea(classes="form-control")
'<textarea class="form-control" name="bio"></textarea>'

>>> form.bio.as_textarea(label="Your bio:")
'<label for="bio">Your bio:</label>\n<textarea id="bio" name="bio"></textarea>'
```


### as_checkbox( )

```python
field.as_checkbox(label=None, **attrs)
```

Renders the field as a `<input type="checkbox">` element.

If you use a `label` argument, a `<label>` will be added *surrounding* the input with a class "checkbox" and the text *after* the checkbox. 

Examples:

```python
>>> form.tos.as_checkbox()
'<input name="tos" type="checkbox">'

>>> form.tos.as_checkbox(classes="form-control")
'<input class="form-control" name="tos" type="checkbox">'

>>> form.tos.as_checkbox(label="I didn’t read this")
'<label class="checkbox"><input name="tos" type="checkbox"> I didn’t read this</label>'
```


### as_radio( )

```python
field.as_radio(label=None, **attrs)
```

Renders the field as a single `<input type="radio">` element.

If you use a `label` argument, a `<label>` will be added *surrounding* the input with a class "radio" and the text *after* the radio button.

Examples:

```python
>>> form.size.as_radio()
'<input name="size" type="radio">'

>>> form.size.as_radio(classes="form-control")
'<input class="form-control" name="size" type="radio">'

>>> form.size.as_radio(label="XL")
'<label class="radio"><input name="size" type="radio"> XL</label>'
```


### as_select_tag( )

```python
field.as_select_tag(label=None, **attrs)
```

Renders *just* the opening `<select>` tag for a field, not any options nor the closing "</select>".

This is intended to be used with `<option>` tags writted by hand or genereated
by other means.

If you use a `label` argument, a `<label>` will be added before the input, and also an `id` attribute to connect both  (that can also be overwritten).

Examples:

```python
>>> form.city.as_select_tag()
'<select name="city">'

# If the field has `multiple=True`
>>> form.city.as_select_tag()
'<select name="city" multiple>'

>>> form.city.as_select_tag(classes="form-control")
'<select class="form-control" name="city">'

>>> form.city.as_select_tag(label="Choose a city")
'<label for="city">Choose a city</label>\n<select name="city">'
```


### as_select( )

```python
field.as_select(items, label=None, **attrs)
```

Renders the field as a `<select>` element.

If you use a `label` argument, a `<label>` will be added before the input, and also an `id` attribute to connect both  (that can also be overwritten).

The `items` argument is a list that can have two type of elements:

1. A tuple of `label, value` for rendering as an `<option>`.

2. A tuple of a label and another list of tuples: `(label, [(label, value), ...])`. This will be rendered as an `<optgroup>` with the label as the title and the items in the list as `<option>`s inside that group.

You can mix the two types of elements to have first-level `<option>` and `<optgroup>`s in the same `<select>`.

Example:

```python
>>> items = [
...     ("Sidney", 21),
...     ("Tokyo", 22),
...     "America", [
...         ("New York", 1),
...         ("San Francisco", 2),
...         ("Buenos Aires", 3),
...         ("Lima", 4),
...         ("Bogota", 5),
...     ],
...     "Europe", [
...       ("Rome", 6),
...       ("London", 7),
...       ("Madrid", 8),
...       ("Paris", 9),
...       ("Berlin", 10),
...     ],
... ]
>>> form.city.as_select(items, label="Choose a city:")
'''
<label for="city">Choose a city:</label>
<select id="city" name="city">
  <option value="">Sidney</option>
  <option value="">Tokyo</option>
  <optgroup label="America">
    <option value="1">New York</option>
    <option value="2">San Francisco</option>
    <option value="3">Buenos Aires</option>
    <option value="4">Lima</option>
    <option value="5">Bogota</option>
  </optgroup>
  <optgroup label="Europe">
    <option value="6">Rome</option>
    <option value="7">London</option>
    <option value="8">Madrid</option>
    <option value="9">Paris</option>
    <option value="10">Berlin</option>
  </optgroup>
</select>
'''
```


### render_optgroup( )

```python
field.render_optgroup(label, items, **attrs)
```

Renders an `<optgroup>` tag with `<options>`. Used by [as_select()](#as_select) to render its groups, but you can call it yourself to build your options list by hand.

The `label` is the title of the group and `items` is a list of `label, value` tuples for the options.

Example:

```python
>>> items = [
...     ("Rome", 6),
...     ("London", 7),
...     ("Madrid", 8),
...     ("Paris", 9),
...     ("Berlin", 10),
... ]
>>> form.city.render_optgroup("Europe", items)
'''
<optgroup label="Europe">
  <option value="6">Rome</option>
  <option value="7">London</option>
  <option value="8">Madrid</option>
  <option value="9">Paris</option>
  <option value="10">Berlin</option>
</optgroup>
'''
```


### render_option( )

```python
field.render_option(label, value=None, **attrs)
```

Renders an `<option>` element. Used by [as_select()](#as_select) and by [render_optgroup()](#render_optgroup) to render its options, but you can call it yourself to build your options list by hand.

If you omit the value, the label will be used as a value as well.

Examples:

```python
>>> form.city.render_option("Lima")
'<option value="Lima">Lima</option>'

>>> form.city.render_option("Lima", 123)
'<option value="123">Lima</option>'

>>> form.city.render_option("Lima", "LIM", data_color="orange")
'<option value="LIM" data-color="orange">Lima</option>'
```


### render_error( )

```python
field.render_error(tag="div", **attrs)
```

If the field has an error, this methods renders a tag (a `<div>` by default)with an "error" class and the error message. Both the tag and the class can be overwritten.

If the field has no error, nothing is rendered.

Examples:

```python
# If the field has a `required` error
>>> form.email.render_error()
'<div class="error">This field is required</div>'

# Custom tag and class
>>> form.email.render_error(tag="p", classes="errorMessage")
'<p class="errorMessage">This field is required</p>'

# If the field has no error
>>> form.name.render_error()
''
```


## Using form templates

Proper Form doesn't have a default `form.render()` method, but you can write one yourself on each of your forms or, better yet, in a base form.

For example you could have a separated template for each if your forms in a `templates/forms/` folder:

```python
from flask import render_template
from proper_form import Form

class BaseForm(Form):
    def render(self):
        name = self.__class__.__name__.lower()
        tmpl = f"forms/{name}.html.jinja2"
        return render_template(tmpl, form=self)
```

If you make all of your forms inherit from that base form, you will now be able of rendering a form just calling its `.render()` method.

```python
class MyForm(BaseForm):
  name = Text()
  ...
```

```jinja
<p>lorem ipsum</p>
{{ myform.render() }}
<p>lorem ipsum</p>
```

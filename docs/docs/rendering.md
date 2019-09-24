
# Rendering fields

Not so long ago, form libraries could get away with recommending a simple

```html+jinja
# Old, inflexible way
<form method="post">{{ form.render() }}</form>
```

It was convenient for many of their users that didn't need or knew about responsive pages, custom styles, or fancy widgets. Forms were expected to be simple after all.

These days, however, it's so limited that is ridiculous. That's why Proper Form doesn't have a magic `render()` method, but instead gives you a series of helpers to make it easy to write how you need to render each field.

The other thing Proper Form do different is that it doesn't tie a field type to a specific HTML tag. You might think an URL field it's always going to be displayed as an `<input>`, but *it doesn't have to*. You could also have URLs as values of checkboxes, radio buttons, or selects, as you choose.


## Available methods

The following are methods *of each field*. Eg: `form.myfield.as_input()` renders something like `<input name="myfield" type="text">`.

### as_input( )

```python
field.as_input(label=None, **attrs)
```


### as_textarea( )

```python
field.as_textarea(label=None, **attrs)
```


### as_checkbox( )

```python
field.as_checkbox(label=None, **attrs)
```


### as_radio( )

```python
field.as_radio(label=None, **attrs)
```


### as_select_tag( )

```python
field.as_select_tag(label=None, **attrs)
```


### as_select( )

```python
field.as_select(items, label=None, **attrs)
```


### render_optgroup( )

```python
field.render_optgroup(label, items, values=None, **attrs)
```


### render_option( )

```python
field.render_option(item, values=None, **attrs)
```


### render_error( )

```python
field.render_error(tag="div", **attrs)
```


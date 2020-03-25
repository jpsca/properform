
# Fields

A field represent a data type. It handles coercing of the input to that data type and following validations. For example, `Text`, `Integer`, `Date`, and `Email` are some of the available fields.

```python
import proper_form as f

class MyForm(f.Form):
    name = f.Text(required=True)
    email = f.Email(required=True)
    birthday = f.Date()
```

Unlike most (all?) the other form libraries, Proper Form doesn't tie a field to a specific HTML representation. For example, an `Email` field can be rendered as a `<input type="email">`, but also as a `<select>`, a `<input type="checkbox">`, etc. The important part is that the received input is normalized and checked to have the shape of an email address, no matter how the input gets to the field.

The most important thing to remember about fields, is that they always take a **list** of input values, even if only one is sent or needed. All received values are processed even if you only need the first one. It does that for several reasons:

1. You can configure any field to take and return a list of values by setting to `True` its `multiple` option.
2. Some special fields work with groups of two separated `<input>`. For example, a `SplittedDateTime` expects to receive at least two values with the same name, and cast the first as a date and the second as a time.
3. Can be used by the `Confirmed` validator to check if a value has been repeated. The classic use is for password confirmation fields.


## Fields common arguments

Each `Field` class constructor takes at least these arguments. Some `Field` classes take additional, field-specific arguments, but the following should always be accepted:

```python
Field(*validators, **options)
```

### `*`validators

Zero or more callables that get the type-casted values and have to return `True` if is ok or `False` if not. Proper Form comes with several pre-made validators (see the [Validators](validators.md) page), but any custom function or callable object can be used.

### required <small>(`False`)</small>

By default, each `Field` class assumes the value is optional, but if you set this option to `True`, an empty value – either None or the empty string ("") – then `validate()` will fail.

### strict <small>(`True`)</small>

By default, if the coercion of the input to the field's data type fails, `validate()` will also fail.
You can ignore it and continue without that value by setting this option to `False`.

Of course, even if this option is set to `False`, if all values are invalid and `required` is `True`, `validate()` will still fails for that other reason.

### multiple <small>(`False`)</small>

Since the input is always a list, and all values are processed, this argument only indicates if the field returns the full list of values or just the first one.

In the HTML, you tipically want this to be `True` for something like a list of checkboxes or a `<select multiple>` tag.

For fields that by default take two values to represent one, like the `SplittedDateTime`, the values will be processed in *pairs*. Example: `["date1", "time1", "date2", "time2", ]`.

### min_num <small>(`None`)</small>

Validates that the number of values with this name is *at least* this.

### max_num <small>(`None`)</small>

Validates that the number of values with this name is *at most* this.

### error_messages <small>(`None`)</small>

The `required`, `strict`, `min_num`, and `max_num` validations fail with this predefined error messages:

```python
default_error_messages = {
    "required": "This field is required.",
    "type": "Invalid type.",
    "min_num": "You need at least {num} values.",
    "max_num": "You can have at most {num} values.",
}
```

The `error_messages` argument allows you to overwrite all or some of these messages by passing a dictionary with your custom error messages for those validations.

### collection <small>(`False`)</small>

This will treat all inputs as a comma-separated list of values, process them, validate them independently, and join them again at the end. Classic examples are lists of emails or URLs

If `strict` is `False`, any value that can't be type-casted is filtered out, so you can end with a valid final result even if some of the input values weren't.

Setting this to `True` forces `multiple` to be `False`, the result will always be comma-separated list of values in a single string.

### sep <small>(`","`)</small>

I wrote "comma-separated", but in fact, a collection will be splitted and joined by whatever character(s) you specify in the `sep` option.

### clean <small>(`None`)</small>

Just before the field return the type-casted and validated values, you might want to adjust them a little more.

This option allows you to pass a function that recieves the final value, or a list of values, if `multiple` is `True`, process it/them in some way and returns it.

For redability, instead of passing it as an argument, you can alternatively define a method in the parent form named `clean_NAME()` for the same effect.

```python
class MyForm(Form):
	# as an argument
	name = Text(clean=lambda v: v.strip("-"))
	mydate = DateTime()

	# as method in the parent form
	def clean_mydate(self, pyvalue):
		# change timezone or something
		...
		return clean_value

```

### prepare <small>(`None`)</small>

Some data types, like dates, need to be converted to strings before can be shown in the HTML. You don't usually have to worry about this because the each field take care of it by default, but in some rare cases, you might need to use your own custom function. This option allows you to pass a function to do that.

The function passed as `prepare`, must take a *stored* value and return a string.

For redability, instead of passing it as an argument, you can alternatively define a method in the parent form named `prepare_NAME()` for the same effect.

```python
class MyForm(Form):
	# as an argument
	name = Text(prepare=lambda v: f"--{v}--")
	mydate = DateTime()

	# as method in the parent form
	def prepare_mydate(self, pyvalue):
		# change timezone or something
		...
		return "some str value"

```

## Field attributes

The attributes of fields can be useful when rendering fields, specially if you need to do something unusual.

### name

The name attribute of the field for the HTML form, setted by the parent `Form` class. 

### required

The same as the attribute.

### values

List of values, already formatted for showing them in the HTML form.

### value

The first of the values or an empty string if none is found.


## Field methods

All field methods are about rendering, so they are covered in the [Rendering page](rendering.md)


## Built-in Field classes

Naturally, Proper Form includes several Field classes that represent common data types needs. This section documents each built-in field.


### Boolean( )

```python
Boolean(*validators, **options)
```

Normalizes to a `True` or `False` value.

A value is normalized to `False` if, stripped and lowercased, is one of `""`, `"none"`, `"0"`, `"no"`, `"nope"`, `"nah"`, `"off"`, or `"false"`. Otherwise is normalized to `True`.


### Date( )

```python
Date(*validators, **options)
```

Validate that the given values are dates with the format `YYYY-MM-dd`.

Normalizes to a `datetime.date` value.

Shows the stored values using the format `YYYY-MM-dd`.


### DateTime( )

```python
DateTime(*validators, **options)
```

Validate that the given values are dates or datetimes with the format `YYYY-MM-dd` plus an optional time. The time can be in a 12-hours or 24-hours format, with or without seconds.

Normalizes to a `datetime.datetime` value.

Shows the stored values using the format `YYYY-MM-dd HH:mm:ss AM/PM` or `YYYY-MM-dd HH:mm AM/PM` if the seconds are zero.


### Email( )

```python
Email(*validators, check_dns=False, allow_smtputf8=False, **options)
```

Validates and normalize an email address using the [python-email-validator](https://github.com/JoshData/python-email-validator) library. Even if the format is valid, it cannot guarantee that the email is real, so the purpose of this validation is to alert the user of a typing mistake.

The normalizations include lowercasing the domain part of the email address (domain names are case-insensitive), and unicode "NFC" normalization of the whole address.

**check_dns** (bool):

Check if the domain name in the email address resolves. This still doesn't guarantee that the email is real, but at least you can discard domain mistypes and completely bogus email addresses.

There is nothing to be gained by trying to actually contact an SMTP server, so that's not done.

**allow_smtputf8** (bool):

Accept non-ASCII characters in the local part of the address (before the @-sign).

This is disabled by default because these email addresses require that your mail submission library and the mail servers along the route to the destination, including your own outbound mail server, all support the [SMTPUTF8 (RFC 6531)](https://tools.ietf.org/html/rfc6531) extension.


### File( )

```python
File(*validators, **options)
```

A field for rendering an `<input type="file">`. Proper Form does not deal with any file handling or validation.


### Float( )

```python
Float(*validators, **options)
```

Normalizes to a float value.


### HexColor( )

```python
HexColor(*validators, **options)
```

Accepts a color in hex, rgb, or rgba color and normalize it to a hex value of 6 digits or 6 digits plus one for alpha.

Examples:

- "#f2e" → "#ff22ee"
- "rgb(255, 0, 255)" → "#ff00ff"
- "rgb(221, 96, 89)" → "#dd6059"
- "rgba(221, 96, 89, 0.3)" → "#dd60594c"


### Integer( )

```python
Integer(*validators, **options)
```

Normalizes to an integer value.


### Month( )

```python
Month(*validators, **options)
```

Validate that the given values are dates with the `YYYY-MM` format. Example: "1980-07".

Normalizes to a `datetime.date` value.

Shows the stored values using the `YYYY-MM` format.


### Password( )

```python
Password(*validators, **options)
```

A text field. Doesn't normalize or validates it.

Whatever value is accepted by this field is not rendered back to the browser like normal fields.


### Slug( )

```python
Slug(
	*validators,
	max_length=0,
	separator='-',
	stopwords=None,
	regex_pattern=None,
	replacements=None,
	lowercase=True,
	word_boundary=False,
	entities=True,
	decimal=True,
	hexadecimal=True,
	**options
)
```

A slug is a short label for something, containing only letters, numbers, underscores, or hyphens. Is tipically used for using a name in a URL.

To do the conversion, this field uses the powerful [python-slugify](https://github.com/un33k/python-slugify) library, so it takes the same arguments:

**max_length** (int):

output string length

**separator** (str):

separator between words

**stopwords** (iterable):

words to discount

**regex_pattern** (str):

regex pattern for allowed characters

**replacements** (iterable):

list of replacement rules e.g. [['|', 'or'], ['%', 'percent']]

**lowercase** (bool):

activate case sensitivity by setting it to False

**word_boundary** (bool):

truncates to end of full words (length may be shorter than max_length)

**entities** (bool):

converts html entities to unicode (foo &amp; bar -> foo-bar)

**decimal** (bool):

converts html decimal to unicode (&#381; -> Ž -> z)

**hexadecimal** (bool):

converts html hexadecimal to unicode (&#x17D; -> Ž -> z)


### SplittedDateTime( )

```python
SplittedDateTime(*validators, **options)
```

A Datetime field splitted in a date and a time field (with the same name). The input values are grouped in pairs, with the first one is the date and the second one the time.

Validates that the first items of the pairs are dates with the format `YYYY-MM-dd`, and the seconds are empty strings (which is equivalent to "00:00") or times in a 12-hours or 24-hours format, with or without seconds.

Normalizes to a `datetime.datetime` value.

Shows the date part of the stored values using the format `YYYY-MM-dd`, and the time parts as `HH:mm:ss AM/PM` or `HH:mm AM/PM` if the seconds are zero.


### Text( )

```python
Text(*validators, **options)
```

A simple text field that normalize the input by stripping the leading and final spaces.


### Time( )

```python
Time(*validators, **options)
```

A 12-hours or 24-hours time field, seconds optional. Examples: "5:03 AM", "11:00 PM", "4:20:16 PM.

Normalizes to a `datetime.time` value.

Shows the stored value as `HH:mm:ss AM/PM` or `HH:mm AM/PM` if the seconds are zero.


### URL( )

```python
URL(*validators, require_tld=False, **options)
```

Validates and normalize an URL address.

Even if the format is valid, it cannot guarantee that the URL is real. The purpose of this function is to alert the user of a typing mistake.

The normalizations include lowercasing (domain names are case-insensitive), and unicode "NFC" normalization.

**require_tld** (bool):

Indicates if the domain-name portion of the URL must contain a .tld suffix. Set this to `True` if you want to disallow domains like `localhost`.


# Validators

Validators are functions that take the list of values of a filed, already type casted, and check if they meet some condition, like a minimum length.

## Built-in validators

HyperForm includes several validators for common data needs. These are technically validator *factories*, because they take some arguments and return a validator as a function, tailored to your specific need. Example:

```python
class MyForm(Form):
	birthday = Date(
		BeforeNow(),  # You need the "()" even without arguments
		After(datetime.date(1900, 1, 1)),
		required=True
	)
```

All of these have default error messages, but you can overwrite them using a `message` attribute if you like.


### After

```python
After(dt, message=None)
```

Works with `Date`, `DateTime`, `SplittedDateTime`, and any other field that cast the values to dates.

Validate that all of the dates happens *after* another one.


### AfterNow

```python
AfterNow(message=None)
```

Works with `Date`, `DateTime`, `SplittedDateTime`, and any other field that cast the values to dates.

Validates that all of the dates happens in the future (the "now" at the moment of the validation).


### Before

```python
Before(dt, message=None)
```

Works with `Date`, `DateTime`, `SplittedDateTime`, and any other field that cast the values to dates.

Validate that all of the dates happens *before* another one.


### BeforeNow

```python
BeforeNow(message=None)
```

Works with `Date`, `DateTime`, `SplittedDateTime`, and any other field that cast the values to dates.

Validates that all of the dates happens in the past (the "now" at the moment of the validation).


### Confirmed

```python
Confirmed(message=None)
```

Validates that a value is identical every time has been repeated. Classic use is for password confirmation fields.

Work with every type of field.


### InRange

```python
InRange(minval, maxval, message=None)
```

Validates that a value is of a minimum (`minval`) and a maximum (`maxval`) value.

This will work with integers, floats, decimals, strings, and any data type that can be compared.


### LessThan

```python
LessThan(value, message=None)
```

Validates that a value is *less or equal* than another `value` (that can be an integer, a float, etc.)

This will work with integers, floats, decimals, strings, and any data type that can be compared.


### MoreThan

```python
MoreThan(value, message=None)
```

Validates that a value is *more or equal* than another (that can be an integer, a float, etc.)

This will work with integers, floats, decimals, strings, and any data type that can be compared.


### LongerThan

```python
LongerThan(length, message=None)
```

Validates the length of a value is *longer or equal* than a minimum `length`.

This will work with strings, and any data type that has a "length".


### ShorterThan

```python
ShorterThan(length, message=None)
```

Validates the length of a value is *shorter or equal* than a maximum `length`.

This will work with strings, and any data type that has a "length".


## Writing your custom validators

Validators are just functions with two properties:

1. They must take a *list* of values
2. The must return `True` if all values "are ok", or a tuple `(False, "error message")` if not.

Let's write a custom validator to see it in practice:

```python
def must_yell(values):
	for value in values:
		if value != value.upper():
			return False, "Please YELL."
	return True
```

And to use in a field, you pass it as an argument, like other validators:

```python
class MyForm(Form):
	message = Text(must_yell, LongerThan(3), required=True)
```

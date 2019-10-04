
# Proper Form Documentation

Proper Form is a python library for modern form input handling and validation.

It tries very hard not to be terrible like all the others:

<blockquote style="max-width:480px; margin:0 auto;">
<p>The main problem I used to have with it was the markup. 
<br>I wanted Bootstrap <em>classes</em>. 
<br>I wanted <em>complex layouts</em> like multiple columns.</p>
<footer>— <cite>Random Redditor</cite></footer>
</blockquote>


## How Proper Form is different

- Your form can have nested subforms, to create or update several objects, in the same page, at once. No need for modals or separated pages.

- Any field can accept multiple values; as a list or as a comma-separated text.

- A field isn't tied to a specific HTML tag, so can be presentend in multiple ways. Even the same form can be used in different contexts and have different widgets and styles on each.

- All error messages are editable. We are not robots, the tone of the messages must be able to change or to be translated.

- Commonly used built-in validators, but you can write a simple function to use a custom one.

- Incredible easy to integrate with any ORM (object-relational mapper). Built-in adaptators for SQLAlchemy and Pony.


## Install

```python
# Create a virtual environment
python -m venv .venv
# Activate said environment
source .venv/bin/activate
# Install the library
pip install proper_form
```

## Key Concepts

- Forms are the core container of Proper Form, they are classes that group fields and/or formsets and, sometimes, connect them to models.
- Fields do most of the heavy lifting. Each field represents a data type and the field handles coercing form the input string to that datatype. They can also run validations on the values.
- Every field can be rendered as any form widget (inputs, selects, checboxes), even if a particular widget don't make sense for the data type.
- In order to specify validation rules, fields contain a list of Validators.
- Formsets are lists of subforms. Additional validations can be added to the minimum and maximum number of forms are allowed. Also, you can control if adding new forms or deleteing old ones is allowed.


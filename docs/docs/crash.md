
# Crash course

## Key Concepts

- `Form`s are the core container of Proper Form, they are classes that group fields and/or formsets and, sometimes, connect them to models.
- Fields do most of the heavy lifting. Each field represents a data type and the field handles coercing form the input string to that datatype. They can also run validations on the values.
- Every field can be rendered as any form widget (inputs, selects, checboxes), even if a particular widget don't make sense for the data type.
- In order to specify validation rules, fields contain a list of validator functions.
- Formsets are lists of subforms. You can control if adding new forms or deleting old ones is allowed.


## Diving into it

This is an example of a simple form connected to a Model:

```python
# forms.py
from proper_form import SQLAForm, Text, LongerThan
from .models import db, Message


class BaseForm(SQLAForm):
    _session = db.session


class MessageForm(BaseForm):
    _model = Message

    your_name = Text(required=True)
    message = Text(
        LongerThan(5, "Please write a longer message"),
        required=True
    )
```

Our form has two text fields, both required. The second one has a validator to ensure that the value is longer than five characters. You can have several validators on each field.

There are three steps involved in using a form.

**[1] First**, we need to show the form to the user. Let's see it with an example in Flask. First, in your controller, we create a form instance using the input data and the existing object (that could be `None`, if it doesn't exist yet):

```python hl_lines="15" tab="Controller"
from flask import request, render_template
from .app import app
from .forms import MessageForm
from .models import db, Message


@app.route("/messages/new/", methods=["GET", "POST"])
@app.route("/messages/<int:msg_id>/edit/", methods=["GET", "POST"])
def edit(msg_id=None):
    # Load the message if exists
    message = None
    if msg_id:
        message = db.query(Message).filter_by(id=msg_id).first()

    form = MessageForm(request.form, message)

    # TODO

    return render_template(
        "message_edit.html.jinja2",
        form=form,
    )
```

```html+jinja tab="Template"
{% extends "layout.html" %}
{% block title %}Edit message{% endblock %}

{% block content %}
<form method="post" action="">
  <div class="form-group">
    {{ form.your_name.as_input(label="Name:") }}
    {{ form.your_name.render_error() }}
  </div>
  <div class="form-group">
    {{ form.message.as_textarea(label="Message:") }}
    {{ form.message.render_error() }}
  </div>
  <button type="submit" class="btn btn-primary">Save</button>
</form>
{% endblock %}
```

**[2] Second**, we process the input data the user send using the form:

```python hl_lines="17 20 21"
from flask import request, render_template, redirect, url_for, flash
from .app import app
from .forms import MessageForm
from .models import db, Message


@app.route("/messages/new/", methods=["GET", "POST"])
@app.route("/messages/<int:msg_id>/edit/", methods=["GET", "POST"])
def edit(msg_id=None):
    if msg_id:
        message = db.query(Message).filter_by(id=msg_id).first()
    else:
        message = None  

    form = MessageForm(request.form, message)
    # [2]
    if request.method == 'POST' and form.validate():
        # [3]
        form.save()
        flash("Message saved.", 'success')
        return redirect(url_for("messages"))

    return render_template(
        "message_edit.html.jinja2",
        form=form,
    )
```

Note that we have it so validate() is only called if there is POST data. The reason we gate the validation check this way is that, when there is no POST data (like in step [1]), we don’t want to cause validation errors.

If the form was submitted and has errors, it'll be shown again to the user, only this time with error messages.

**[3] Finally**, if the form is valid, we do something with the data. In this example, `form.save()` creates/update a `Message` object in the database. After we finish processing the form, we do a redirect to another page.

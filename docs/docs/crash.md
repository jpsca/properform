
# Crash course

This is an example of a simple form:

```python
# forms.py
from proper_form import Form, Email, Text, LongerThan
from .models import Message


class MessageForm(Form):
    _model = Message

    your_name = Text(required=True)
    message = Text(
        LongerThan(5, "Please write a longer message"),
        required=True
    )
```

Our form has two text fields, both required. The second one has a validator to ensure that the value is longer than five characters. You can have several validators on each field.

There are three steps steps to use a form.

**[1] First**, we need to show the form to the user. Let's see it with an example in Flask. First, in your controller, we create a form instance using the input data and the existing object data (that could be `None`, if it doesn't exist yet):

```python hl_lines="16" tab="Controller"
from flask import request, render_template
from .app import app
from .forms import MessageForm
from .models import db, Message


@app.route("/messages/new/", methods=["GET", "POST"])
@app.route("/messages/<int:msg_id>/edit/", methods=["GET", "POST"])
def edit(msg_id=None):
    # Load the message if exists
    if msg_id:
        message = db.query(Message).filter_by(id=msg_id).first()
    else:
        message = None  

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
    if request.method == 'POST' and form.is_valid:
        # [3]
        form.save()
        flash("Message saved.", 'success')
        return redirect(url_for("messages"))

    return render_template(
        "message_edit.html.jinja2",
        form=form,
    )
```

We know the form has been submitted because the methos is "POST" instead of "GET". If the form has error it'll be  shown again to the user, only this time with erros messages.

**[3] Finally**, if the form is valid, we do something with the data. In this example, `form.save()` creates/update a `Message` object in the database. After we finish processing the form, we do a redirect to another page.

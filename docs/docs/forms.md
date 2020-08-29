
# Forms

At the heart of HyperForm is the `Form` class. A form contain your field definitions, delegate validation, take input, and in general function as the glue holding everything together.

Form are classes that inherit from the `hyperform.Form` class. You then create instances of those classes in your controllers, using the request and maybe object data.

```python
from hyperform  import Form, Email, Password

class LoginForm(Form):
    login = Email(required=True)
    password = Password(required=True)

def login():
    form = LoginForm(request.POST)
    if request.method == "POST" and form.validate():
        ...
    return render_template("login.html", form=form)

```

## Form attributes

```python
Form(input_data=None, object=None, file_data=None, *, prefix="")
```

### input_data

A *MultiDict* containing the data from a form request.
Form requests are typically POST requests and many web frameworks returns it under the name `request.POST`.

### object

Pre-existing data used to populate the form. This can be a dictionary or an instance of a class, typically an ORM Model.

### file_data

Optional *MultiDict* with the file data. In some web frameworks this data can be read from the rest of the POST data, so you don't need to (or can) include it again here.

In other frameworks, like Flask, this data is called `request.files`.

### prefix

Optional namespace for the form.


## Form methods

### validate()

[ TODO ]

### save()

[ TODO ]

### create_object()

[ TODO ]

### update_object()

[ TODO ]

### delete_object()

[ TODO ]

### load_data()

This method can be used to replace the data passed when instantiating the form.
Eg:

```python
form = Form()
...
form.load_data(input_data, object_data)
```

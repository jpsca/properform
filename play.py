from multidict import MultiDict
import wtforms as f
from wtforms import validators as v


class MyForm(f.Form):
    first_name = f.StringField("First Name", validators=[v.input_required()])
    last_name = f.StringField("Last Name", validators=[v.optional()])


data = MultiDict({"first_name": "Juan Pablo", "last_name": "Scaletti"})
data = MultiDict()


class MyObject(object):
    first_name = "Juan Pablo"
    last_name = "Scaletti"


obj = MyObject()

form = MyForm(data, obj)

print(form.validate())

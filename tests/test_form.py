import hyperform as f
from hyperform.constants import SEP, DELETED


def test_declare_form():
    class ContactForm(f.Form):
        subject = f.Text(required=True)
        email = f.Email()
        message = f.Text(required=True, error_messages={"required": "write something!"})

    form = ContactForm()

    assert sorted(form._fields) == [
        "email",
        "message",
        "subject",
    ]
    assert form.updated_fields is None
    assert form.subject.name == "subject"
    assert form.email.name == "email"
    assert form.message.name == "message"


def test_form_independence():
    class AForm(f.Form):
        afield = f.Text()

    form1 = AForm({"afield": "1"})
    form2 = AForm({"afield": "2"})
    form3 = AForm({"afield": "3"})

    assert form1.afield != form2.afield
    assert form1.afield != form3.afield
    assert form2.afield != form3.afield

    assert form1.afield.value == "1"
    assert form2.afield.value == "2"
    assert form3.afield.value == "3"


def test_form_independence_same_input():
    class AForm(f.Form):
        afield = f.Text()

    input_data = {"afield": "text"}
    form1 = AForm(input_data)
    form2 = AForm(input_data)
    form3 = AForm(input_data)

    assert form1.afield != form2.afield
    assert form1.afield != form3.afield
    assert form2.afield != form3.afield


def test_form_independence_prefixes():
    class AForm(f.Form):
        afield = f.Text()

    input_data = {
        f"f1{SEP}afield": "1",
        f"f2{SEP}afield": "2",
        f"f3{SEP}afield": "3",
    }
    form1 = AForm(input_data, prefix="f1")
    form2 = AForm(input_data, prefix="f2")
    form3 = AForm(input_data, prefix="f3")

    assert form1.afield != form2.afield
    assert form1.afield != form3.afield
    assert form2.afield != form3.afield

    assert form1.afield.value == "1"
    assert form2.afield.value == "2"
    assert form3.afield.value == "3"


def test_declare_form_with_prefix():
    class ContactForm(f.Form):
        subject = f.Text(required=True)
        email = f.Email()
        message = f.Text(required=True, error_messages={"required": "write something!"})

    form = ContactForm(prefix="myform")

    assert sorted(form._fields) == [
        "email",
        "message",
        "subject",
    ]
    assert form.subject.name == f"myform{SEP}subject"
    assert form.email.name == f"myform{SEP}email"
    assert form.message.name == f"myform{SEP}message"


def test_validate_empty_form():
    class MyForm(f.Form):
        lorem = f.Text()
        ipsum = f.Text()

    form = MyForm()
    assert form.validate() == {"lorem": None, "ipsum": None}
    assert form.updated_fields == []


def test_validate_blank_form():
    class MyForm(f.Form):
        lorem = f.Text()
        ipsum = f.Text()

    form = MyForm({"lorem": "", "ipsum": ""})
    assert form.validate() == {"lorem": "", "ipsum": ""}
    assert sorted(form.updated_fields) == ["ipsum", "lorem"]


def test_validate_optional_form():
    class MyForm(f.Form):
        lorem = f.Text()
        ipsum = f.Text()

    form = MyForm({"lorem": "foo", "ipsum": "bar"})
    assert form.validate() == {"lorem": "foo", "ipsum": "bar"}
    assert sorted(form.updated_fields) == ["ipsum", "lorem"]


def test_load_object():
    class ContactForm(f.Form):
        subject = f.Text(required=True)
        email = f.Email()
        message = f.Text(required=True)

    data = {
        "subject": "Hello world",
        "email": "hello@world.com",
        "message": "Lorem ipsum.",
    }
    form = ContactForm({}, data)
    assert form.subject.value == data["subject"]
    assert form.email.value == data["email"]
    assert form.message.value == data["message"]


def test_load_object_instance():
    class ContactForm(f.Form):
        subject = f.Text(required=True)
        email = f.Email()
        message = f.Text(required=True)

    class MyObject(object):
        subject = "Hello world"
        email = "hello@world.com"
        message = "Lorem ipsum."

    obj = MyObject()

    form = ContactForm({}, obj)
    assert form.subject.value == obj.subject
    assert form.email.value == obj.email
    assert form.message.value == obj.message


def test_validate_form_input():
    class ContactForm(f.Form):
        subject = f.Text(required=True)
        email = f.Email()
        message = f.Text(required=True)

    data = {
        "subject": "Hello world",
        "email": "hello@world.com",
        "message": "Lorem ipsum.",
    }
    form = ContactForm(data)
    assert form.validate() == data


def test_do_not_validate_form_object():
    class ContactForm(f.Form):
        subject = f.Text(required=True)
        email = f.Email()
        message = f.Text(required=True)

    class MyObject(object):
        subject = "Hello world"
        email = "hello@world.com"
        message = "Lorem ipsum."

    obj = MyObject()

    form = ContactForm({}, obj)
    assert form.validate() is None


def test_validate_form_error():
    class ContactForm(f.Form):
        subject = f.Text(required=True)
        email = f.Email()
        message = f.Text(required=True, error_messages={"required": "write something!"})

    form = ContactForm({"email": "hello@world.com"})
    assert form.validate() is None
    assert form.subject.error == "This field is required."
    assert form.message.error == "write something!"


def test_idempotent_valid_is_valid():
    class MyForm(f.Form):
        lorem = f.Text()

    form = MyForm()
    assert form.validate()
    assert form.validate()
    assert form.validate()


def test_idempotent_invalid_is_valid():
    class MyForm(f.Form):
        lorem = f.Text(required=True)

    form = MyForm()
    assert form.validate() is None
    assert form.validate() is None
    assert form.validate() is None


def test_updated_fields_from_empty():
    class MyForm(f.Form):
        a = f.Text()
        b = f.Text()
        c = f.Text()
        d = f.Text()

    form = MyForm({"b": "foo", "d": "bar"})
    assert form.validate()
    assert sorted(form.updated_fields) == ["b", "d"]


def test_updated_fields_from_object():
    class MyForm(f.Form):
        a = f.Text()
        b = f.Text()
        c = f.Text()
        d = f.Text()

    form = MyForm(
        {"a": "a", "b": "new", "c": "c", "d": "new"},
        {"a": "a", "b": "b", "c": "c", "d": "d"},
    )
    assert form.validate()
    assert sorted(form.updated_fields) == ["b", "d"]


def test_load_clean_and_prepare():
    class MyForm(f.Form):
        meh = f.Text()

        def prepare_meh(self, object_value):
            return [object_value]

        def clean_meh(self, pyvalues):
            return pyvalues

    form = MyForm()

    assert form.meh.custom_prepare == form.prepare_meh
    assert form.meh.custom_clean == form.clean_meh


def test_dont_overwrite_field_clean_and_prepare():
    def field_prepare(self, object_value):
        return [object_value]

    def field_clean(self, pyvalues):
        return pyvalues

    class MyForm(f.Form):
        meh = f.Text(prepare=field_prepare, clean=field_clean)

        def prepare_meh(self, object_value):
            return [object_value]

        def clean_meh(self, pyvalues):
            return pyvalues

    form = MyForm()

    assert form.meh.custom_prepare == field_prepare
    assert form.meh.custom_clean == field_clean


def test_cant_delete_by_default():
    class ContactForm(f.Form):
        subject = f.Text(required=True)
        email = f.Email()
        message = f.Text(required=True)

    data = {
        DELETED: "1",
        "subject": "Hello world",
        "email": "hello@world.com",
        "message": "Lorem ipsum.",
    }
    form = ContactForm(data)

    assert not form._deleted
    assert form.subject.value == data["subject"]
    assert form.email.value == data["email"]
    assert form.message.value == data["message"]

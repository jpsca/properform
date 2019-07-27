import proper_form as f


def test_declare_form():
    class ContactForm(f.Form):
        subject = f.Text(required=True)
        email = f.Email()
        message = f.Text(required=True, error_messages={"required": "write something!"})

    form = ContactForm()

    assert sorted(form._fields) == ["email", "message", "subject", ]
    assert form.errors is None
    assert form.valid_data is None
    assert form.updated_fields is None
    assert form.deleted_fields is None

    assert form.subject.name == "subject"
    assert form.email.name == "email"
    assert form.message.name == "message"


def test_declare_form_with_prefix():
    class ContactForm(f.Form):
        subject = f.Text(required=True)
        email = f.Email()
        message = f.Text(required=True, error_messages={"required": "write something!"})

    form = ContactForm(prefix="myform")

    assert sorted(form._fields) == ["email", "message", "subject", ]
    assert form.subject.name == "myform.subject"
    assert form.email.name == "myform.email"
    assert form.message.name == "myform.message"


def test_validate_empty_form():
    class MyForm(f.Form):
        lorem = f.Text()
        ipsum = f.Text()

    form = MyForm()
    assert form.is_valid
    assert form.validate() == {"lorem": None, "ipsum": None}
    assert form.errors is None
    assert form.updated_fields == []
    assert form.deleted_fields == []


def test_validate_blank_form():
    class MyForm(f.Form):
        lorem = f.Text()
        ipsum = f.Text()

    form = MyForm({"lorem": "", "ipsum": ""})
    assert form.is_valid
    assert form.validate() == {"lorem": "", "ipsum": ""}
    assert form.errors is None
    assert sorted(form.updated_fields) == ["ipsum", "lorem"]
    assert form.deleted_fields == []


def test_validate_optional_form():
    class MyForm(f.Form):
        lorem = f.Text()
        ipsum = f.Text()

    form = MyForm({"lorem": "foo", "ipsum": "bar"})
    assert form.is_valid
    assert form.validate() == {"lorem": "foo", "ipsum": "bar"}
    assert form.errors is None
    assert sorted(form.updated_fields) == ["ipsum", "lorem"]
    assert form.deleted_fields == []


def test_validate_form():
    class ContactForm(f.Form):
        subject = f.Text(required=True)
        email = f.Email()
        message = f.Text(required=True, error_messages={"required": "write something!"})

    data = {
        "subject": "Hello world",
        "email": "hello@world.com",
        "message": "Lorem ipsum.",
    }
    form = ContactForm(data)
    assert form.validate() == data
    assert form.errors is None


def test_validate_form_error():
    class ContactForm(f.Form):
        subject = f.Text(required=True)
        email = f.Email()
        message = f.Text(required=True, error_messages={"required": "write something!"})

    form = ContactForm({"email": "hello@world.com"})
    assert form.validate() is None
    assert form.errors == {
        "subject": "This field is required.",
        "message": "write something!",
    }


def test_idempotent_valid_is_valid():
    class MyForm(f.Form):
        lorem = f.Text()

    form = MyForm()
    assert form.is_valid
    assert form.is_valid
    assert form.validate()
    assert form.is_valid
    assert form.validate()


def test_idempotent_invalid_is_valid():
    class MyForm(f.Form):
        lorem = f.Text(required=True)

    form = MyForm()
    assert not form.is_valid
    assert not form.is_valid
    assert form.validate() is None
    assert not form.is_valid
    assert form.validate() is None


def test_updated_fields_from_empty():
    class MyForm(f.Form):
        a = f.Text()
        b = f.Text()
        c = f.Text()
        d = f.Text()

    form = MyForm({"b": "foo", "d": "bar"})
    assert form.is_valid
    assert sorted(form.updated_fields) == ["b", "d"]


def test_updated_fields_from_object():
    class MyForm(f.Form):
        a = f.Text()
        b = f.Text()
        c = f.Text()
        d = f.Text()

    form = MyForm(
        {"a": "a", "b": "new", "c": "c", "d": "new"},
        {"a": "a", "b": "b", "c": "c", "d": "d"}
    )
    assert form.is_valid
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

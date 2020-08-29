import hyperform as f
from hyperform.constants import SEP, NEW


def test_declare_form_set():
    class SectionForm(f.Form):
        title = f.Text()
        body = f.Text()

    class WrapperForm(f.Form):
        title = f.Text()
        sections = f.FormSet(SectionForm)

    form = WrapperForm(prefix="myform")
    assert form.title.name == f"myform{SEP}title"
    assert form.sections
    assert form.sections[0].title.name == f"myform.sections{SEP}{NEW}1{SEP}title"
    assert form.validate()
    assert not form.sections.updated


def test_extra():
    class SectionForm(f.Form):
        title = f.Text()
        body = f.Text()

    class WrapperForm(f.Form):
        sections = f.FormSet(SectionForm, extra=3)

    form = WrapperForm()
    assert len(form.sections) == 3
    assert [sf.prefix for sf in form.sections._forms] == [
        f"sections{SEP}{NEW}1",
        f"sections{SEP}{NEW}2",
        f"sections{SEP}{NEW}3",
    ]


def test_can_create_disable_extra():
    class SectionForm(f.Form):
        title = f.Text()
        body = f.Text()

    class WrapperForm(f.Form):
        sections = f.FormSet(SectionForm, extra=3, can_create=False)

    form = WrapperForm()
    assert len(form.sections._forms) == 0


def test_form_independence_inside_form_set():
    class SectionForm(f.Form):
        title = f.Text()
        body = f.Text()

    class WrapperForm(f.Form):
        sections = f.FormSet(SectionForm, extra=3)

    form = WrapperForm()
    form1 = form.sections[0]
    form2 = form.sections[1]
    form3 = form.sections[2]

    assert form1 != form2
    assert form1 != form3
    assert form2 != form3

    assert form1.title != form2.title
    assert form1.title != form3.title
    assert form2.title != form3.title


def test_forms_independence_in_different_form_sets():
    class SectionForm(f.Form):
        title = f.Text()
        body = f.Text()

    class WrapperForm(f.Form):
        sections = f.FormSet(SectionForm)

    form1 = WrapperForm()
    form2 = WrapperForm()
    form3 = WrapperForm()

    assert form1.sections[0] != form2.sections[0]
    assert form1.sections[0] != form3.sections[0]
    assert form2.sections[0] != form3.sections[0]

    assert form1.sections[0].title != form2.sections[0].title
    assert form1.sections[0].title != form3.sections[0].title
    assert form2.sections[0].title != form3.sections[0].title


def test_form_set_load_fieldset_data():
    class SectionForm(f.Form):
        title = f.Text(required=True)
        body = f.Text()

    class WrapperForm(f.Form):
        title = f.Text(required=True)
        sections = f.FormSet(SectionForm)

    input_data = {
        "title": "Wrapper title",
        f"sections{SEP}{NEW}1{SEP}title": "title 1",
        f"sections{SEP}{NEW}1{SEP}body": "body 1",
        f"sections{SEP}{NEW}2{SEP}title": "title 2",
        f"sections{SEP}{NEW}2{SEP}body": "body 2",
        f"sections{SEP}{NEW}3{SEP}body": "body 3",
    }
    form = WrapperForm(input_data)
    form1 = form.sections[0]
    form2 = form.sections[1]
    form3 = form.sections[2]

    assert len(form.sections) == 3

    assert form1 != form2
    assert form1 != form3
    assert form2 != form3

    assert form1.title != form2.title
    assert form1.title != form3.title
    assert form2.title != form3.title

    assert form1.body != form2.body
    assert form1.body != form3.body
    assert form2.body != form3.body

    assert form1.prefix == f"sections{SEP}{NEW}1"
    assert form2.prefix == f"sections{SEP}{NEW}2"
    assert form3.prefix == f"sections{SEP}{NEW}3"

    assert form1.title.value == "title 1"
    assert form1.body.value == "body 1"

    assert form2.title.value == "title 2"
    assert form2.body.value == "body 2"

    assert form3.title.value == ""
    assert form3.body.value == "body 3"


def test_form_set_validate():
    class SectionForm(f.Form):
        title = f.Text(required=True)
        body = f.Text()

    class WrapperForm(f.Form):
        title = f.Text(required=True)
        sections = f.FormSet(SectionForm)

    input_data = {
        "title": "Wrapper title",
        f"sections{SEP}{NEW}1{SEP}title": "title 1",
        f"sections{SEP}{NEW}2{SEP}title": "title 2",
        f"sections{SEP}{NEW}3{SEP}title": "title 3",
    }
    form = WrapperForm(input_data)
    assert form.validate()
    assert form.sections.updated


def test_form_set_validate_invalid_subform():
    class SectionForm(f.Form):
        title = f.Text(required=True)
        body = f.Text()

    class WrapperForm(f.Form):
        title = f.Text(required=True)
        sections = f.FormSet(SectionForm)

    input_data = {
        "title": "Wrapper title",
        f"sections{SEP}{NEW}1{SEP}title": "title 1",
        f"sections{SEP}{NEW}1{SEP}body": "body 1",
        f"sections{SEP}{NEW}2{SEP}title": "title 2",
        f"sections{SEP}{NEW}2{SEP}body": "body 2",
        f"sections{SEP}{NEW}3{SEP}body": "body 3",
    }
    form = WrapperForm(input_data)

    assert len(form.sections) == 3

    form1 = form.sections[0]
    form2 = form.sections[1]
    form3 = form.sections[2]
    assert form1.title.value == "title 1"
    assert form1.body.value == "body 1"
    assert form2.title.value == "title 2"
    assert form2.body.value == "body 2"
    assert form3.title.value == ""
    assert form3.body.value == "body 3"

    assert form.validate() is None


def test_min_num_forms():
    class SectionForm(f.Form):
        title = f.Text()

    class WrapperForm(f.Form):
        sections = f.FormSet(SectionForm, min_num=4)

    input_data = {
        f"sections{SEP}{NEW}1{SEP}title": "title 1",
        f"sections{SEP}{NEW}2{SEP}title": "title 2",
        f"sections{SEP}{NEW}3{SEP}title": "title 3",
    }
    form = WrapperForm(input_data)

    assert len(form.sections) == 3
    assert form.validate() is None
    assert form.sections.error == "Please submit at least 4 forms."


def test_max_num_forms():
    class SectionForm(f.Form):
        title = f.Text()

    class WrapperForm(f.Form):
        sections = f.FormSet(SectionForm, max_num=2)

    input_data = {
        f"sections{SEP}{NEW}1{SEP}title": "title 1",
        f"sections{SEP}{NEW}2{SEP}title": "title 2",
        f"sections{SEP}{NEW}3{SEP}title": "title 3",
    }
    form = WrapperForm(input_data)

    assert len(form.sections) == 3
    assert form.validate() is None
    assert form.sections.error == "Please submit at most 2 forms."

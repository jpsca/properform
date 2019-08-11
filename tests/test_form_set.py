import proper_form as f
from proper_form.constants import SEP, NEW


class SectionForm(f.Form):
    title = f.Text()
    body = f.Text()


def test_declare_form_set():
    class WrapperForm(f.Form):
        title = f.Text()
        sections = f.FormSet(SectionForm)

    form = WrapperForm(prefix="myform")
    assert form.title.name == f"myform{SEP}title"
    assert form.sections._forms[0].title.name == f"myform.sections{SEP}{NEW}1{SEP}title"


def test_extra():
    class WrapperForm(f.Form):
        sections = f.FormSet(SectionForm, extra=3)

    form = WrapperForm()
    assert len(form.sections._forms) == 3
    assert [sf.prefix for sf in form.sections._forms] == [
        f"sections{SEP}{NEW}1",
        f"sections{SEP}{NEW}2",
        f"sections{SEP}{NEW}3",
    ]


def test_can_create_disable_extra():
    class WrapperForm(f.Form):
        sections = f.FormSet(SectionForm, extra=3, can_create=False)

    form = WrapperForm()
    assert len(form.sections._forms) == 0


# def test_form_set_validate():
#     class WrapperForm(f.Form):
#         title = f.Text()
#         sections = f.FormSet(SectionForm)

#     d =

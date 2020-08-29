import pytest

from hyperform.ftypes import type_email


VALID_EMAILS = [
    "juanpablo@example.com",
    "juan+pablo@example.com",
    "juan.pablo@example.com",
    "jps@nic.pe",
    "my.common.email+proper@gmail.com",

    # from https://en.wikipedia.org/wiki/International_email
    "Abc@example.com",
    "Abc.123@example.com",
    "user+mailbox/department=shipping@example.com",
    "!#$%&'*+-/=?^_`.{|}~@example.com",

    # International domains
    "test@mañana.com",
    "ivan@екзампл.ком",
]

VALID_UTF8_EMAILS = [
    "mañana@mañana.com",
    "伊昭傑@郵件.商務",
    "राम@मोहन.ईन्फो",
    "юзер@екзампл.ком",
    "θσερ@εχαμπλε.ψομ",
]

INVALID_EMAILS = [
    "",
    "lalala",
    "aa@a",
    "fail@test,com",
    "Wrapped <a@example.com>",

    "my@.leadingdot.com",
    "my@．．leadingfwdot.com",
    "my@..twodots.com",
    "my@twodots..com",
    "my@baddash.-.com",
    "my@baddash.-a.com",
    "my@baddash.b-.com",
    ".leadingdot@domain.com",
    "..twodots@domain.com",
    "twodots..here@domain.com",
    "me@⒈wouldbeinvalid.com",
]


@pytest.mark.parametrize("value", VALID_EMAILS)
def test_type_email_valid(value):
    assert type_email(value) == value


@pytest.mark.parametrize("value", INVALID_EMAILS)
def test_type_email_invalid(value):
    assert type_email(value) is None


@pytest.mark.parametrize("value", VALID_UTF8_EMAILS)
def test_type_email_invalid_with_smtputf8(value):
    assert type_email(value, allow_smtputf8=True) == value


@pytest.mark.parametrize("value", VALID_UTF8_EMAILS)
def test_type_email_invalid_without_smtputf8(value):
    assert type_email(value, allow_smtputf8=False) is None

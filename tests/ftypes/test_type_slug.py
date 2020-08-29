from hyperform.ftypes import type_slug


def test_slugify():
    txt = "This is a test ---"
    r = type_slug(txt)
    assert r == "this-is-a-test"

    txt = "影師嗎"
    r = type_slug(txt)
    assert r == "ying-shi-ma"

    txt = "C'est déjà l'été."
    r = type_slug(txt)
    assert r == "c-est-deja-l-ete"

    txt = "Nín hǎo. Wǒ shì zhōng guó rén"
    r = type_slug(txt)
    assert r == "nin-hao-wo-shi-zhong-guo-ren"

    txt = "Компьютер"
    r = type_slug(txt)
    assert r == "kompiuter"

    txt = "jaja---lol-méméméoo--a"
    r = type_slug(txt, max_length=9)
    assert r == "jaja-lol"

    txt = "jaja---lol-méméméoo--a"
    r = type_slug(txt, max_length=15, word_boundary=True)
    assert r == "jaja-lol-a"

    txt = "jaja---lol-méméméoo--a"
    r = type_slug(txt, max_length=20, word_boundary=True, separator=".")
    assert r == "jaja.lol.mememeoo.a"

    txt = "one two three four five"
    r = type_slug(txt, max_length=13, word_boundary=True)
    assert r == "one-two-three"

    txt = "the quick brown fox jumps over the lazy dog"
    r = type_slug(txt, stopwords=["the"])
    assert r == "quick-brown-fox-jumps-over-lazy-dog"

    txt = "the quick brown fox jumps over the lazy dog in a hurry"
    r = type_slug(txt, stopwords=["the", "in", "a", "hurry"])
    assert r == "quick-brown-fox-jumps-over-lazy-dog"

    txt = "thIs Has a stopword Stopword"
    r = type_slug(txt, stopwords=["Stopword"], lowercase=False)
    assert r == "thIs-Has-a-stopword"

    txt = "___This is a test___"
    regex_pattern = r"[^-a-z0-9_]+"
    r = type_slug(txt, regex_pattern=regex_pattern)
    assert r == "___this-is-a-test___"

    txt = "___This is a test___"
    regex_pattern = r"[^-a-z0-9_]+"
    r = type_slug(txt, separator="_", regex_pattern=regex_pattern)
    assert r != "_this_is_a_test_"

    txt = "10 | 20 %"
    r = type_slug(txt, replacements=[["|", "or"], ["%", "percent"]])
    assert r == "10-or-20-percent"

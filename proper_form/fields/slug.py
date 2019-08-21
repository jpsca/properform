from ..types import type_slug

from .text import Text


__all__ = ("Slug",)


class Slug(Text):
    """A slug is a short label for something, containing only letters, numbers,
    underscores or hyphens.

    Uses `python-slugify` to do the conversion so it takes the same arguments:

        max_length (int):
            output string length

        separator (str):
            separator between words

        stopwords (iterable):
            words to discount

        regex_pattern (str):
            regex pattern for allowed characters

        replacements (iterable):
            list of replacement rules e.g. [['|', 'or'], ['%', 'percent']]

        lowercase (bool):
            activate case sensitivity by setting it to False

        word_boundary (bool):
            truncates to end of full words (length may be shorter than max_length)

        entities (bool):
            converts html entities to unicode (foo &amp; bar -> foo-bar)

        decimal (bool):
            converts html decimal to unicode (&#381; -> Ž -> z)

        hexadecimal (bool):
            converts html hexadecimal to unicode (&#x17D; -> Ž -> z)

    """

    def __init__(
        self,
        *validators,
        max_length=0,
        separator='-',
        stopwords=None,
        regex_pattern=None,
        replacements=None,
        lowercase=True,
        word_boundary=False,
        entities=True,
        decimal=True,
        hexadecimal=True,
        **kwargs
    ):
        super().__init__(
            *validators,
            max_length=max_length or 0,
            separator=separator,
            stopwords=stopwords,
            regex_pattern=regex_pattern,
            replacements=replacements,
            lowercase=lowercase,
            word_boundary=word_boundary,
            entities=entities,
            decimal=decimal,
            hexadecimal=hexadecimal,
            **kwargs
        )

    def type(self, value, **options):
        return type_slug(value, **options)

from .field import Field

from ..types import type_url


__all__ = ("URL", )


class URL(Field):
    """Validates and normalize an URL address.

    Even if the format is valid, it cannot guarantee that the URL is real. The
    purpose of this function is to alert the user of a typing mistake.

    Perform an UTS-46 normalization of the domain, which includes lowercasing
    (domain names are case-insensitive), NFC normalization, and converting all label
    separators (the period/full stop, fullwidth full stop, ideographic full stop, and
    halfwidth ideographic full stop) to basic periods. It will also raise an exception
    if there is an invalid character in the input, such as "⒈" which is invalid
    because it would expand to include a period.

    Options:

        require_tld (bool):
            If the domain-name portion of the URL must contain a .tld
            suffix. Set this to `True` if you want to disallow domains like
            `localhost`.

    """

    type = type_url

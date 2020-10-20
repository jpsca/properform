import re
from urllib.parse import urlsplit, urlunsplit

import idna


__all__ = ("type_url", )

rx_scheme = re.compile(r"^[a-z]{3,7}://[^/]")
rx_url = r"^([a-z]{3,7}://)?([^./:][^/:]+[^./:]%s|([0-9]{1,3}\.){3}[0-9]{1,3})(:[0-9]+)?(\/.*)?$"  # noqa: E501
rx_tld = r"\.[a-z]{2,10}"


def type_url(value, require_tld=False):
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
    rx = re.compile(rx_url % (rx_tld if require_tld else ""), re.IGNORECASE)
    if not rx.match(value):
        return None

    if not rx_scheme.match(value):
        # Check for possible typos
        if value.startswith(("http//", "http:/", "http:///", "http:")):
            return None
        value = "http://" + value

    scheme, domain, path, query, fragment = urlsplit(value)

    if ".." in domain or "//" in domain:
        return None

    try:
        domain = idna.uts46_remap(domain, std3_rules=False, transitional=False)
    except idna.IDNAError:  # pragma: no cover
        return None

    return urlunsplit((scheme, domain, path, query, fragment))

from email_validator import validate_email


__all__ = ("type_email", )


def type_email(value, check_dns=False, allow_smtputf8=False):
    """Validates and normalize an email address using the
    JoshData/python-email-validator library.

    Even if the format is valid, it cannot guarantee that the email is real. The
    purpose of this function is to alert the user of a typing mistake.

    The normalizations include lowercasing the domain part of the email address
    (domain names are case-insensitive), Unicode "NFC" normalization of the whole
    address (which turns characters plus combining characters into precomposed
    characters where possible and replaces certain Unicode characters (such as
    angstrom and ohm) with other equivalent code points (a-with-ring and omega,
    respectively)), replacement of fullwidth and halfwidth characters in the domain
    part, and possibly other UTS46 mappings on the domain part.

    Options:

        check_dns (bool):
            Check if the domain name in the email address resolves.
            There is nothing to be gained by trying to actually contact an SMTP server,
            so that's not done.

        allow_smtputf8 (bool):
            Accept non-ASCII characters in the local part of the address
            (before the @-sign). These email addresses require that your mail
            submission library and the mail servers along the route to the destination,
            including your own outbound mail server, all support the
            [SMTPUTF8 (RFC 6531)](https://tools.ietf.org/html/rfc6531) extension.
            By default this is set to `False`.

    """
    try:
        v = validate_email(
            value,
            check_deliverability=check_dns,
            allow_smtputf8=allow_smtputf8,
        )
        return v["email"]
    except (ValueError, TypeError):
        return None

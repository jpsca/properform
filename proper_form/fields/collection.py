import re

from .bases import BaseMultiField


class Collection(BaseMultiField):
    r"""A field that takes an open number of values of the same kind.
    For example, a list of comma separated tags or email addresses.

    Arguments are:

        sep (str):
            String to separate each value. Default is ",".
    """

    # We want to recieve a single value, hence this is False, but to process
    # multiple values, so we inherit from `BaseMultiField`.
    multi = True

    def __init__(self, type, *validators, sep=",", **kwargs):
        self.sep = sep
        super().__init__(type, *validators, **kwargs)

    def _pre(self, value):
        rxsep = r"\s*%s\s*" % re.escape(self.sep.strip())
        return re.split(value, rxsep)

    def _post(self, values):
        return self.sep.join(values)

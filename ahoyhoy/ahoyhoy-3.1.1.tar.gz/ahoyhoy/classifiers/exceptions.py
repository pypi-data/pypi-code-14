from requests.exceptions import HTTPError


class AhoyhoyClassifiersException(Exception):
    """
    Exception for general usage.
    """
    pass


class Ahoyhoy500Exception(AhoyhoyClassifiersException, HTTPError):
    pass

class AhoyhoyLbException(Exception):
    """
    Exception for general usage.
    """
    pass


class URLIsUnresolvedException(AhoyhoyLbException):
    pass


class LbNoEndpointsException(AhoyhoyLbException):
    """No Endpoints in the closed state."""
    pass
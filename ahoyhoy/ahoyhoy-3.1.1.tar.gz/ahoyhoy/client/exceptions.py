from requests.exceptions import RequestException


class AhoyhoyClientException(Exception):
    """
    Exception for general usage.
    """
    pass


class AhoyhoyRequestsException(AhoyhoyClientException, RequestException):
    """Request failed for any reason"""
    pass


class NoAvailableEndpointsClientException(AhoyhoyClientException):
    """No Endpoints in the closed state, even after lists updates."""
    pass

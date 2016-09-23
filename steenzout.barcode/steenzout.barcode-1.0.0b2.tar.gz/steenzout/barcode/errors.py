# -*- coding: utf-8 -*-
"""Exceptions module."""


class BarcodeError(Exception):

    """Base class for steenzout.barcode exceptions."""

    def __init__(self, msg):
        self.msg = msg
        super(BarcodeError, self).__init__()

    def __str__(self):
        """Returns a string representation of this object.

        Returns:
            (str): string representation of this object.
        """
        return self.msg


class IllegalCharacterError(BarcodeError):
    """Raised when a bar code contains illegal characters."""

    def __init__(self, allowed):
        super(IllegalCharacterError, self).__init__('Bar code can only contain %s' % allowed)


class BarcodeNotFoundError(BarcodeError):
    """Raised when an unknown barcode is requested."""

    def __init__(self, name):
        self.name = name
        super(BarcodeNotFoundError, self).__init__(
            'The barcode {0!r} you requested is not known.'.format(self.name)
        )


class NumberOfDigitsError(BarcodeError):
    """Raised when the number of digits do not match."""


class WrongCountryCodeError(BarcodeError):
    """Raised when a JAN (Japan Article Number) doesn't start with
    450-459 or 490-499.
    """

    def __init__(self, country):
        self.country = country
        super(WrongCountryCodeError, self).__init__(
            'Country code %s isn\'t between 450-460 or 490-500.' % self.country
        )

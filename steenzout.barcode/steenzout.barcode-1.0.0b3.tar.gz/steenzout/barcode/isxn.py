# -*- coding: utf-8 -*-
"""ISXN module.

:Provided barcodes: ISBN-13, ISBN-10, ISSN

This module provides some special codes, which are no standalone bar codes.

All codes where transformed to EAN-13 barcodes.

In every case, the checksum is new calculated.

Example::

    >>> from steenzout.barcode import get_barcode
    >>> ISBN = get_barcode('isbn10')
    >>> isbn = ISBN('0132354187')
    >>> unicode(isbn)
    u'0132354187'
    >>> isbn.get_fullcode()
    u'9780132354189'
    >>> # Test with wrong checksum
    >>> isbn = ISBN('0132354180')
    >>> unicode(isbn)
    u'0132354187'
"""

from .ean import EAN13
from .errors import IllegalCharacterError, WrongCountryCodeError


class ISBN13(EAN13):
    """Class for ISBN-13 bar codes.

    Args:
        isbn (str): ISBN number.
        writer (:py:class:`.writer.BaseWriter`): instance of writer class to render the bar code.
    """

    name = 'ISBN-13'
    digits = 13

    def __init__(self, isbn, writer=None):
        super(ISBN13, self).__init__(isbn.replace('-', ''), writer)

    @staticmethod
    def calculate_checksum(code):
        return None

    @staticmethod
    def validate(code):
        if code[:3] not in ('978', '979'):
            # raise WrongCountryCodeError('ISBN must start with 978 or 979.')
            raise WrongCountryCodeError(code[:3])

        if not code.isdigit():
            raise IllegalCharacterError('[0-9]{%d}' % ISBN13.digits)

        if len(code) != ISBN13.digits:
            raise ValueError('Bar code %s requires %d digits' % (code, ISBN13.digits))


class ISBN10(ISBN13):
    """Class for ISBN-10 bar codes.

    Args:
        code (str): ISBN number.
        writer (:py:class:`.writer.BaseWriter`): instance of writer class to render the bar code.
    """

    name = 'ISBN-10'

    digits = 10

    def __init__(self, code, writer=None):
        super(ISBN10, self).__init__(code.replace('-', ''), writer)

    @staticmethod
    def calculate_checksum(code):
        tmp = sum([x * int(y) for x, y in enumerate(code[:9], start=1)]) % 11

        if tmp == 10:
            return 'X'
        else:
            return tmp

    @staticmethod
    def validate(code):
        if not code.isdigit():
            raise IllegalCharacterError('[0-9]{%d}' % ISBN10.digits)

        if len(code) != ISBN10.digits:
            raise ValueError('Bar code %s requires %d digits' % (code, ISBN10.digits))

    def isbn13(self):
        """Returns the ISBN-13 representation of the ISBN-10 bar code.

        Returns:
            (:py:class:`ISBN13`): ISBN-13 representation of the bar code.
        """
        return ISBN13('978%s' % self.code, writer=self.writer)

    def ean13(self):
        """Returns the EAN-13 representation of the ISBN-10 bar code.

        Returns:
            (:py:class:`EAN13`): EAN-13 representation of the bar code.
        """
        return EAN13('978%s' % self.code, writer=self.writer)


class ISSN(EAN13):
    """Class for ISSN bar codes.

    This code is rendered as EAN-13 by prefixing it with 977 and
    adding 00 between code and checksum.

    Args:
        issn (str): issn number.
        writer (:py:class:`.writer.BaseWriter`): instance of writer class to render the bar code.
    """

    name = 'ISSN'

    digits = 8

    def __init__(self, issn, writer=None):
        super(ISSN, self).__init__(issn.replace('-', ''), writer)

    @staticmethod
    def calculate_checksum(code):
        tmp = 11 - sum([x * int(y) for x, y in enumerate(reversed(code[:7]), start=2)]) % 11

        if tmp == 10:
            return 'X'
        else:
            return tmp

    @staticmethod
    def validate(code):
        if len(code) != ISSN.digits:
            raise ValueError('Bar code %s requires %d digits' % (code, ISSN.digits))

        if not code[:-1].isdigit():
            raise IllegalCharacterError('[0-9]{%d}[0-9X]{1}' % (ISSN.digits - 1))

        if code[-1] != 'X' and not code[-1].isdigit():
            raise IllegalCharacterError('[0-9]{%d}[0-9X]{1}' % (ISSN.digits - 1))

    def build(self):
        """Builds the barcode pattern from `self.ean`.

        Returns:
            (str): The pattern as string.
        """
        return self.ean13().build()

    def ean13(self):
        """Returns the EAN-13 representation of the ISSN bar code.

        Returns:
            (:py:class:`EAN13`): EAN-13 representation of the bar code.
        """
        ean13_code = '977%s00' % self.code[:7]
        return EAN13('%s%s' % (ean13_code, EAN13.calculate_checksum(ean13_code)), writer=self.writer)


# Shortcuts
InternationalStandardBookNumber13 = ISBN13
InternationalStandardBookNumber10 = ISBN10
InternationalStandardSerialNumber = ISSN

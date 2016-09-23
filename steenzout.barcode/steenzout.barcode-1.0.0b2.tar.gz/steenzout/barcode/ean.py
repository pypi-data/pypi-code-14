# -*- coding: utf-8 -*-
"""Module: barcode.ean

:Provided barcodes: EAN-13, EAN-8, JAN
"""

from functools import reduce

from .base import Barcode
from .charsets import ean as _ean
from .errors import IllegalCharacterError, WrongCountryCodeError
from .helpers import sum_chars

# EAN13 Specs (all sizes in mm)
SIZES = dict(
    SC0=0.27, SC1=0.297, SC2=0.33, SC3=0.363, SC4=0.396,
    SC5=0.445, SC6=0.495, SC7=0.544, SC8=0.61, SC9=0.66
)


class EAN13(Barcode):
    """Class for EAN13 bar codes.

    Attributes:
        checksum (int): EAN checksum.

    Args:
        ean (str): the EAN number.
        writer (:py:class:`.writer.BaseWriter`): instance of writer class to render the bar code.
    """

    name = 'EAN-13'

    digits = 13

    def __init__(self, code, writer=None):
        super(EAN13, self).__init__(code, writer)

    def __unicode__(self):
        return self.code

    __str__ = __unicode__

    @staticmethod
    def calculate_checksum(code):
        """Calculates a EAN-13 code checksum.

        Args:
            code (str): EAN-13 code.

        Returns:
            (integer): the checksum for `self.ean`.
        """
        sum_odd = reduce(sum_chars, code[:-1:2])
        sum_even = reduce(sum_chars, code[1::2])

        return (10 - ((sum_odd + sum_even * 3) % 10)) % 10

    @staticmethod
    def validate(code):
        """Calculates a EAN-13 code checksum.

        Args:
            code (str): EAN-13 code.

        Raises:
            IllegalCharacterError in case the bar code contains illegal characters.
            ValueError in case the bar code exceeds its maximum length or
                if the checksum digit doesn't match.
        """
        if not code.isdigit():
            raise IllegalCharacterError('[0-9]{%d}' % EAN13.digits)

        if len(code) != EAN13.digits:
            raise ValueError('Bar code %s requires %d digits' % (code, EAN13.digits))

        checksum = EAN13.calculate_checksum(code)
        if checksum != int(code[-1]):
            raise ValueError('Checksum character mismatch %s != %s' % (checksum, code[-1]))

    def build(self):
        """Builds the barcode pattern from `self.ean`.

        Returns:
            (str): The pattern as string.
        """
        code = _ean.EDGE[:]
        pattern = _ean.LEFT_PATTERN[int(self.code[0])]

        for i, number in enumerate(self.code[1:7]):
            code += _ean.CODES[pattern[i]][int(number)]
        code = '%s%s' % (code, _ean.MIDDLE)

        for number in self.code[7:]:
            code += _ean.CODES['C'][int(number)]

        return ['%s%s' % (code, _ean.EDGE)]

    def get_fullcode(self):
        return self._code

    def render(self, writer_options=None):
        options = dict(module_width=SIZES['SC2'])
        options.update(writer_options or {})
        return Barcode.render(self, options)

    def to_ascii(self):
        """Returns an ascii representation of the barcode.

        Returns:
            (str): ascii representation of the barcode.
        """
        code = self.build()
        for i, line in enumerate(code):
            code[i] = line.replace('1', '|').replace('0', ' ')
        return '\n'.join(code)


class JAN(EAN13):
    """Class for JAN bar codes.

    Args:
        code (str): the jan number.
        writer (:py:class:`.writer.BaseWriter`): instance of writer class to render the bar code.
    """

    name = 'JAN'

    valid_country_codes = list(range(450, 460)) + list(range(490, 500))

    def __init__(self, code, writer=None):
        if int(code[:3]) not in JapanArticleNumber.valid_country_codes:
            raise WrongCountryCodeError(code[:3])
        super(JAN, self).__init__(code, writer)


class EAN8(EAN13):
    """Class for EAN-8 bar codes.

    See :py:class:`EAN-13` for details.

    :parameters:
        code (str): EAN-8 number.
        writer (:py:class:`.writer.BaseWriter`): instance of writer class to render the bar code.
    """

    name = 'EAN-8'

    digits = 8

    def __init__(self, code, writer=None):
        super(EAN8, self).__init__(code, writer)

    @staticmethod
    def calculate_checksum(code):
        """Calculates an EAN-8 code checksum.

        Args:
            code (str): EAN-8 code.

        Returns:
            (int): EAN checksum.
        """
        sum_odd = reduce(sum_chars, code[::2])
        sum_even = reduce(sum_chars, code[1:-1:2])

        return (10 - ((sum_odd * 3 + sum_even) % 10)) % 10

    @staticmethod
    def validate(code):
        """Calculates a EAN-8 code checksum.

        Args:
            code (str): EAN-8 code.

        Raises:
            IllegalCharacterError in case the bar code contains illegal characters.
            ValueError in case the bar code exceeds its maximum length or
                if the checksum digit doesn't match..
        """
        if not code.isdigit():
            raise IllegalCharacterError('[0-9]{%d}' % EAN8.digits)

        if len(code) != EAN8.digits:
            raise ValueError('Bar code %s requires %d digits' % (code, EAN8.digits))

        checksum = EAN8.calculate_checksum(code)

        if checksum != int(code[-1]):
            raise ValueError('Checksum character mismatch %d != %s' % (checksum, code[-1]))

    def build(self):
        """Builds the barcode pattern from `self.ean`.

        Returns:
            (str): string representation of the pattern.
        """
        code = _ean.EDGE[:]

        for number in self.code[:4]:
            code = '%s%s' % (code, _ean.CODES['A'][int(number)])
        code = '%s%s' % (code, _ean.MIDDLE)

        for number in self.code[4:]:
            code = '%s%s' % (code, _ean.CODES['C'][int(number)])

        return ['%s%s' % (code, _ean.EDGE)]


# Shortcuts
EuropeanArticleNumber13 = EAN13
EuropeanArticleNumber8 = EAN8
JapanArticleNumber = JAN

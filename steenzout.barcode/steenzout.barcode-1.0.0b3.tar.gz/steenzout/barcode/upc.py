# -*- coding: utf-8 -*-
"""UPC module.

:Provided barcodes: UPC-A
"""

from functools import reduce

from .base import Barcode
from .charsets import upc as _upc
from .errors import IllegalCharacterError
from .helpers import sum_chars


class UPCA(Barcode):
    """Class for UPC-A bar codes.

    Args:
        code (str): UPC-A bar code.
        writer (:py:class:`.writer.BaseWriter`): instance of writer class to render the bar code.
    """

    name = 'UPC-A'

    digits = 12

    def __init__(self, code, writer=None):
        super(UniversalProductCodeA, self).__init__(code, writer)

    @staticmethod
    def calculate_checksum(code):
        """Calculates the UPC-A checksum.

        Args:
            code (str): UPC-A code.

        Returns:
            (int): UPC-A checksum.
        """

        sum_odd = reduce(sum_chars, code[::2])
        sum_even = reduce(sum_chars, code[1:-1:2])
        check = (sum_even + sum_odd * 3) % 10

        if check == 0:
            return 0
        else:
            return 10 - check

    @staticmethod
    def validate(code):
        """Calculates a UPC-A code checksum.

        Args:
            code (str): UPC-A code.

        Raises:
            IllegalCharacterError in case the bar code contains illegal characters.
            ValueError in case the bar code exceeds its maximum length or
                if the checksum digit doesn't match.
        """
        if not code.isdigit():
            raise IllegalCharacterError('[0-9]{%d}' % UPCA.digits)

        if len(code) != UPCA.digits:
            raise ValueError('Bar code %s requires %d digits' % (code, UPCA.digits))

        checksum = UPCA.calculate_checksum(code)
        if checksum != int(code[-1]):
            raise ValueError('Checksum character mismatch %s != %s' % (checksum, code[-1]))

    def build(self):
        """Builds the bar code pattern.

        Returns:
            (str): the bar code pattern.
        """
        code = _upc.EDGE[:]

        for _, number in enumerate(self.code[0:6]):
            code += _upc.CODES['L'][int(number)]

        code += _upc.MIDDLE

        for number in self.code[6:]:
            code += _upc.CODES['R'][int(number)]

        code += _upc.EDGE

        return [code]

    def to_ascii(self):
        """Returns an ASCII representation of the bar code.

        Returns:
            (str): ASCII representation of the bar code.
        """
        code = self.build()
        for i, line in enumerate(code):
            code[i] = line.replace('1', '|').replace('0', '_')
        return '\n'.join(code)

    def render(self, writer_options=None):
        options = dict(module_width=0.33)
        options.update(writer_options or {})

        return super(UPCA, self).render(options)

    def get_fullcode(self):
        return self._code

UniversalProductCodeA = UPCA

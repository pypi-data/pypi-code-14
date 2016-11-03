# -*- coding: utf-8 -*-
"""Module: barcode.codex

:Provided barcodes: Code 39, Code 128, PZN
"""

from .base import Barcode
from .charsets import code128, code39
from .errors import BarcodeError, IllegalCharacterError


# Sizes
MIN_SIZE = 0.2
MIN_QUIET_ZONE = 2.54


def check_code(code, name, allowed):
    wrong = []
    for char in code:
        if char not in allowed:
            wrong.append(char)
    if wrong:
        raise IllegalCharacterError(
            'The following characters are not valid for %s: %s' % (name, ', '.join(wrong)))


class Code39(Barcode):
    """Initializes a new Code39 instance.

    Attributes:
        code (str):
        writer (:py:class:`.writer.BaseWriter`): writer class.

    Args:
        code (str):
            Code 39 string without \* and checksum (added automatically if `add_checksum` is True).
        writer (:py:class:`.writer Instance`): instance of writer class to render the bar code.
        add_checksum (bool): add the checksum to code or not.
    """

    name = 'Code 39'

    def __init__(self, code, writer=None):
        super(Code39, self).__init__(code.upper(), writer)

    def get_fullcode(self):
        return self.code

    @staticmethod
    def calculate_checksum(code):
        check = sum([code39.MAP[x][0] for x in code]) % 43
        for k, v in code39.MAP.items():
            if check == v[0]:
                return k

    @staticmethod
    def validate(code):
        check_code(code, Code39.name, code39.REF)

    def build(self):
        chars = [code39.EDGE]
        for char in self.code:
            chars.append(code39.MAP[char][1])
        chars.append(code39.EDGE)
        return [code39.MIDDLE.join(chars)]

    def render(self, writer_options=None):
        options = dict(module_width=MIN_SIZE, quiet_zone=MIN_QUIET_ZONE)
        options.update(writer_options or {})
        return Barcode.render(self, options)


class PZN(Code39):
    """Initializes new German number for pharmaceutical products.

    Args:
        pzn (str): code to render.
        writer (:py:class:`.writer.BaseWriter`): instance of writer class to render the bar code.
    """

    name = 'Pharmazentralnummer'

    digits = 6

    def __init__(self, code, writer=None):
        super(PZN, self).__init__(code, writer)

    def get_fullcode(self):
        return 'PZN-%s' % self.code

    @staticmethod
    def calculate_checksum(code):
        sum_ = sum([int(x) * int(y) for x, y in enumerate(code, start=2)])
        checksum = sum_ % 11
        if checksum == 10:
            raise BarcodeError('Checksum can not be 10 for PZN.')
        else:
            return checksum

    @staticmethod
    def validate(code):

        if not code.isdigit():
            raise IllegalCharacterError('[0-9]{%d}' % PZN.digits)

        if len(code) != PZN.digits:
            raise ValueError('Bar code %s exceeds maximum number of characters/digits (%d)' % (code, PZN.digits))

        check_code(code, PZN.name, code39.REF)

    def build(self):
        return self.code39().build()

    def code39(self):
        return Code39('PZN-%s' % self.code, self.writer)


class Code128(Barcode):
    """Initializes a new Code128 instance. The checksum is added automatically
    when building the bars.

    Args:
        code (str): code 128 string without checksum (added automatically).
        writer (:py:class:`.writer.BaseWriter`): instance of writer class to render the bar code.
    """

    name = 'Code 128'

    def __init__(self, code, writer=None):
        self._charset = 'B'
        self._buffer = ''

        super(Code128, self).__init__(code, writer)

    def __unicode__(self):
        return self.code

    __str__ = __unicode__

    @staticmethod
    def calculate_checksum(code):
        return None

    @staticmethod
    def validate(code):
        check_code(code, Code128.name, code128.ALL)

    @property
    def encoded(self):
        return self._build()

    def get_fullcode(self):
        return self.code

    def _new_charset(self, which):
        if which == 'A':
            code = self._convert('TO_A')
        elif which == 'B':
            code = self._convert('TO_B')
        elif which == 'C':
            code = self._convert('TO_C')
        self._charset = which
        return [code]

    def _maybe_switch_charset(self, pos):
        char = self.code[pos]
        next_ = self.code[pos:pos + 10]

        def look_next():
            digits = 0
            for c in next_:
                if c.isdigit():
                    digits += 1
                else:
                    break
            return digits > 3

        codes = []
        if self._charset == 'C' and not char.isdigit():
            if char in code128.B:
                codes = self._new_charset('B')
            elif char in code128.A:
                codes = self._new_charset('A')
            if len(self._buffer) == 1:
                codes.append(self._convert(self._buffer[0]))
                self._buffer = ''
        elif self._charset == 'B':
            if look_next():
                codes = self._new_charset('C')
            elif char not in code128.B:
                if char in code128.A:
                    codes = self._new_charset('A')
        elif self._charset == 'A':
            if look_next():
                codes = self._new_charset('C')
            elif char not in code128.A:
                if char in code128.B:
                    codes = self._new_charset('B')
        return codes

    def _convert(self, char):
        if self._charset == 'A':
            return code128.A[char]
        elif self._charset == 'B':
            return code128.B[char]
        elif self._charset == 'C':
            if char in code128.C:
                return code128.C[char]
            elif char.isdigit():
                self._buffer += char
                if len(self._buffer) == 2:
                    value = int(self._buffer)
                    self._buffer = ''
                    return value

    def _build(self):
        encoded = [code128.START_CODES[self._charset]]
        for i, char in enumerate(self.code):
            encoded.extend(self._maybe_switch_charset(i))
            code_num = self._convert(char)
            if code_num is not None:
                encoded.append(code_num)
            # Finally look in the buffer
        if len(self._buffer) == 1:
            encoded.extend(self._new_charset('B'))
            encoded.append(self._convert(self._buffer[0]))
            self._buffer = ''
        encoded = _try_to_optimize(encoded)
        return encoded

    def build(self):
        encoded = self._build()
        encoded.append(_calculate_checksum(encoded))
        code = ''
        for code_num in encoded:
            code += code128.CODES[code_num]
        code += code128.STOP
        code += '11'
        return [code]

    def render(self, writer_options=None):
        options = dict(module_width=MIN_SIZE, quiet_zone=MIN_QUIET_ZONE)
        options.update(writer_options or {})
        return Barcode.render(self, options)


def _calculate_checksum(encoded):
    out = [encoded[0]]
    for i, code_num in enumerate(encoded[1:], start=1):
        out.append(i * code_num)
    return sum(out) % 103


def _try_to_optimize(encoded):
    if encoded[1] in code128.TO:
        encoded[:2] = [code128.TO[encoded[1]]]
    return encoded

"""
Some helpers for the internal ClickHouse protocol via :9000.
"""


def varint_length(x):
    return sum(x >= r for r in (0, 1 << 7, 1 << 14, 1 << 21, 1 << 28, 1 << 35, 1 << 42, 1 << 49, 1 << 56))


def int2varint(x):
    y = x
    result = []

    for _ in range(8):
        b = y & 0x7f
        if y > 0x7f:
            b = b | 0x80

        result.append(b)

        y = y >> 7

        if not y:
            return ''.join(map(chr, result))


def varint2int(x):
    result = 0

    for i, b in enumerate(x):
        result = result | (ord(b) & 0x7f) << (7 * i)

        if not (ord(b) & 0x80):
            return result


# We could try and send '\x00\npython-cli\x00\x01\x00\x00' to 9000 instead.

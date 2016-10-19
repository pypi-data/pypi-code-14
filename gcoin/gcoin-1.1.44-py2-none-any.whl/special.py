import binascii


def string_to_bytes(s):
    if isinstance(s, bytes):
        return s
    else:
        return s.encode('utf8')


def byte_to_int(b):
    return ord(b)


def bytes_to_hex_string(b):
    return binascii.hexlify(b).encode()


def int_to_byte(i):
    if 0 <= i < 256:
        return chr(i)
    else:
        raise ValueError("int_to_byte arg not in range(256)")



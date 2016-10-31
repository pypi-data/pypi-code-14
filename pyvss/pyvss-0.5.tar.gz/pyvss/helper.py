"""
This helper module contains complimentary functions
to the :py:mod:`pyvss.manager` module
"""
import base64
import gzip

try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO


def compress_encode_string(string_data):
    """
    Compresses and encodes in base64 a given
    string

    :param string_data: string to compress and encode
    :type string_data: str
    :return: compressed and encoded string
    """
    out = StringIO()
    with gzip.GzipFile(fileobj=out, mode='w') as f:
        f.write(string_data)
    return base64.b64encode(out.getvalue()).decode()


def decode_uncompress_string(string_gz_encoded):
    """
    Decompress and decodes a given string

    :param string_gz_encoded: string to decompress and decode
    :type string_gz_encoded: str
    :return: string
    """
    string_gz = base64.b64decode(string_gz_encoded)
    file_obj = StringIO(string_gz)
    return gzip.GzipFile(mode='rb', fileobj=file_obj).read()

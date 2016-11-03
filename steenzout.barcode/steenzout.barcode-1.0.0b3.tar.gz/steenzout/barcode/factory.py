# -*- coding: utf-8 -*-
"""Factory module."""

import six

from .codex import Code39, PZN, Code128
from .ean import EAN8, EAN13, JAN
from .errors import BarcodeNotFoundError
from .isxn import ISBN10, ISBN13, ISSN
from .upc import UPCA

MAPPINGS = dict(
    ean8=EAN8,
    ean13=EAN13,
    ean=EAN13,
    gtin=EAN13,
    jan=JAN,
    upc=UPCA,
    upca=UPCA,
    isbn=ISBN13,
    isbn13=ISBN13,
    gs1=ISBN13,
    isbn10=ISBN10,
    issn=ISSN,
    code39=Code39,
    pzn=PZN,
    code128=Code128,
)


def create_instance(name, code, writer=None):
    """Return bar code instance.

    Args:
        name (str): bar code name.
        code (str): code text.
        writer (:py:class:`steenzout.barcode.writer.Interface`): writer instance.

    Raises:
        (:py:class:`BarcodeNotFoundError`): when the bar code encoding name is invalid or
            the encoding is not implemented.

    Returns:
        (:py:class:`steenzout.barcode.base.Base`): bar code instance.
    """
    if name is None or not isinstance(name, six.string_types):
        raise BarcodeNotFoundError(name)

    if name.lower() in MAPPINGS:
        return MAPPINGS[name.lower()](code, writer)
    else:
        raise BarcodeNotFoundError(name)

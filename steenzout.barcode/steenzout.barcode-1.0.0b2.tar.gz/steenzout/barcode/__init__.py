# -*- coding: utf-8 -*-
"""This package provides a simple way to create standard bar codes.

It needs no external packages to be installed,
the bar codes are created as SVG objects.

If PIL (Python Imaging Library) is installed,
the bar codes can also be rendered as images
(all formats supported by PIL).
"""

from six import string_types

from .errors import BarcodeNotFoundError
from .metadata import __version__

PIL_ENABLED = False


try:
    import PIL
    PIL_ENABLED = True
except ImportError:
    pass


def encodings():
    """Return bar code encodings available.

    Returns:
        (list[str]): available bar code encodings.
    """
    from . import factory
    return factory.MAPPINGS.keys()


def formats():
    """Return image formats available.

    Returns:
        (list['str']): available image formats.
    """
    if PIL_ENABLED:
        return 'BMP', 'EPS', 'GIF', 'JPEG', 'MSP', 'PCX', 'PNG', 'SVG', 'TIFF', 'XBM'
    else:
        return 'EPS', 'SVG'


def generate(name, code, writer=None, output=None, writer_options=None):
    """Generates a file containing an image of the bar code.

    Args:
        name (str): bar code name.
        code (str): bar code.
        writer (:py:class:`steenzout.barcode.writer.Interface`): writer instance.
        output (str): filename of output.
        writer_options (dict): options for the writer class.

    Raises:
        (:py:class:`BarcodeNotFoundError`): when the bar code encoding name is invalid or
            the encoding is not implemented.
    """
    from . import factory

    options = writer_options or {}
    barcode = factory.create_instance(name, code, writer)

    if isinstance(output, string_types):
        return barcode.save(output, options)
    else:
        barcode.write(output, options)


def version():
    """Returns package version.

    Returns:
        (str): package version.
    """
    return __version__

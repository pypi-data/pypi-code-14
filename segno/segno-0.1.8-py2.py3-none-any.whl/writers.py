# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 -- Lars Heuer - Semagia <http://www.semagia.com/>.
# All rights reserved.
#
# License: BSD License
#
"""\
Standard serializers and utility functions for serializers.

The serializers are independent of the :py:class:`segno.QRCode` class,
they just need a matrix (tuple of bytearrays) and the version constant.
"""
from __future__ import absolute_import, unicode_literals, division
import io
import re
import math
import zlib
import codecs
import base64
import gzip
from functools import partial
from xml.sax.saxutils import quoteattr, escape
from struct import pack
from itertools import chain
from functools import reduce
import time
_PY2 = False
try:  # pragma: no cover
    from itertools import zip_longest
    from urllib.parse import quote
except ImportError:  # pragma: no cover
    _PY2 = True
    from itertools import izip_longest as zip_longest
    from urllib import quote
    range = xrange
    str = unicode
    from io import open
from .colors import invert_color, color_to_rgb, color_to_rgb_or_rgba, \
        color_to_webcolor, color_is_black, color_is_white
from .utils import matrix_to_lines, get_symbol_size, get_border, \
        check_valid_scale, check_valid_border, matrix_iter

# Standard creator name
CREATOR = 'Segno <https://pypi.python.org/pypi/segno/>'


def get_writable(file_or_path, mode, encoding=None):
    """\
    Returns a writable stream and if the caller must close the writable
    stream explicitly.

    :param file_or_path: Either a file-like object or a filename.
    :param str mode: String indicating the writing mode (i.e. ``'wb'``)
    :rtype: tuple: fileobj, bool
    """
    try:
        file_or_path.write
        if encoding is None:
            return file_or_path, False
        return codecs.getwriter(encoding)(file_or_path), False
    except AttributeError:
        return open(file_or_path, mode, encoding=encoding), True


def write_svg(matrix, version, out, scale=1, border=None, color='#000',
              background=None, xmldecl=True, svgns=True, title=None, desc=None,
              svgid=None, svgclass='segno', lineclass='qrline', omitsize=False,
              unit=None, encoding='utf-8', svgversion=None, nl=True):
    """\
    Serializes the QR Code as SVG document.

    :param matrix: The matrix to serialize.
    :param int version: The (Micro) QR code version
    :param out: Filename or a file-like object supporting to write bytes.
    :param scale: Indicates the size of a single module (default: 1 which
            corresponds to 1 x 1 pixel per module).
    :param int border: Integer / float indicating the size of the
            quiet zone.
            If set to ``None`` (default), the recommended border size
            will be used (``4`` for QR Codes, ``2`` for a Micro QR Codes).
    :param color: Color of the modules (default: ``#000``). Any value
            which is supported by SVG can be used. In addition, ``None``
            is a valid value. The resulting path won't have a ``stroke``
            attribute.
    :param background: Optional background color (default: ``None`` = no
            background color). See `color` for valid values.
    :param bool xmldecl: Inidcates if the XML declaration header should be
            written (default: ``True``)
    :param bool svgns: Indicates if the SVG namespace should be written
            (default: ``True``).
    :param str title: Optional title of the generated SVG document.
    :param str desc: Optional description of the generated SVG document.
    :param svgid: The ID of the SVG document (if set to ``None`` (default),
            the SVG element won't have an ID).
    :param svgclass: The CSS class of the SVG document
            (if set to ``None``, the SVG element won't have a class).
    :param lineclass: The CSS class of the path element (which draws the
            "black" modules (if set to ``None``, the path won't have a class).
    :param bool omitsize: Indicates if width and height attributes should be
            omitted (default: ``False``). If these attributes are omitted,
            a ``viewBox`` attribute will be added to the document.
    :param str unit: Unit for width / height and other coordinates.
            By default, the unit is unspecified and all values are
            in the user space.
            Valid values: em, ex, px, pt, pc, cm, mm, in, and percentages
    :param str encoding: Encoding of the XML document. "utf-8" by default.
    :param float svgversion: SVG version (default: None)
    :param bool nl: Indicates if the document should have a trailing newline
            (default: ``True``)
    """
    check_valid_scale(scale)
    check_valid_border(border)
    unit = unit or ''
    if unit and omitsize:
        raise ValueError('The unit "{0}" has no effect if the size '
                         '(width and height) is omitted.'.format(unit))
    f, must_close = get_writable(out, 'wt', encoding=encoding)
    write = f.write
    # Write the document header
    if xmldecl:
        write('<?xml version="1.0" encoding="{0}"?>\n'.format(encoding))
    write('<svg')
    if svgns:
        write(' xmlns="http://www.w3.org/2000/svg"')
    if svgversion is not None:
        write(' version={0}'.format(quoteattr(str(svgversion))))
    border = get_border(version, border)
    width, height = get_symbol_size(version, scale, border)
    if not omitsize:
        write(' width="{0}{2}" height="{1}{2}"'.format(width, height, unit))
    if omitsize or unit:
        write(' viewBox="0 0 {0} {1}"'.format(width, height))
    if svgid:
        write(' id={0}'.format(quoteattr(svgid)))
    if svgclass:
        write(' class={0}'.format(quoteattr(svgclass)))
    write('>')
    if title is not None:
        write('<title>{0}</title>'.format(escape(title)))
    if desc is not None:
        write('<desc>{0}</desc>'.format(escape(desc)))
    allow_css3_colors = svgversion is not None and svgversion >= 2.0
    if background is not None:
        bg_color = color_to_webcolor(background, allow_css3_colors=allow_css3_colors)
        fill_opacity = ''
        if isinstance(bg_color, tuple):
            bg_color, opacity = bg_color
            fill_opacity = ' fill-opacity={0}'.format(quoteattr(str(opacity)))
        write('<path fill="{0}"{1} d="M0 0h{2}v{3}h-{2}z"/>'
              .format(bg_color, fill_opacity, width, height))
    write('<path')
    if scale != 1:
        write(' transform="scale({0})"'.format(scale))
    if color is not None:
        opacity = None
        stroke_color = color_to_webcolor(color, allow_css3_colors=allow_css3_colors)
        if isinstance(stroke_color, tuple):
            stroke_color, opacity = stroke_color
        write(' stroke={0}'.format(quoteattr(stroke_color)))
        if opacity is not None:
            write(' stroke-opacity={0}'.format(quoteattr(str(opacity))))
    if lineclass:
        write(' class={0}'.format(quoteattr(lineclass)))
    write(' d="')
    # Current pen pointer position
    x, y = border, border + .5  # .5 == stroke-width / 2
    line_iter = matrix_to_lines(matrix, x, y)
    # 1st coord is absolute
    (x1, y1), (x2, y2) = next(line_iter)
    coord = ['M{0} {1}h{2}'.format(x1, y1, x2 - x1)]
    append_coord = coord.append
    x, y = x2, y2
    for (x1, y1), (x2, y2) in line_iter:
        append_coord('m{0} {1}h{2}'.format(x1 - x, int(y1 - y), x2 - x1))
        x, y = x2, y2
    write(''.join(coord))
    # Close path and doc
    write('"/></svg>')
    if nl:
        write('\n')
    if must_close:
        f.close()


_replace_quotes = partial(re.compile(br'(=)"([^"]+)"').sub, br"\1'\2'")

def as_svg_data_uri(matrix, version, scale=1, border=None, color='#000',
                    background=None, xmldecl=False, svgns=True, title=None,
                    desc=None, svgid=None, svgclass='segno',
                    lineclass='qrline', omitsize=False, unit='',
                    encoding='utf-8', svgversion=None, nl=False,
                    encode_minimal=False, omit_charset=False):
    """\
    Converts the matrix to a SVG data URI.

    The XML declaration is omitted by default (set ``xmldecl`` to ``True``
    to enable it), further the newline is omitted by default (set ``nl`` to
    ``True`` to enable it).

    Aside from the missing ``out`` parameter and the different ``xmldecl``
    and ``nl`` default values and the additional parameter ``encode_minimal``
    and ``omit_charset`` this function uses the same parameters as the
    usual SVG serializer.

    :param bool encode_minimal: Indicates if the resulting data URI should
                    use minimal percent encoding (disabled by default).
    :param bool omit_charset: Indicates if the ``;charset=...`` should be omitted
                    (disabled by default)
    :rtype: str
    """
    encode = partial(quote, safe=b"") if not encode_minimal else partial(quote, safe=b" :/='")
    buff = io.BytesIO()
    write_svg(matrix, version, buff, scale=scale, color=color, background=background,
              border=border, xmldecl=xmldecl, svgns=svgns, title=title,
              desc=desc, svgclass=svgclass, lineclass=lineclass,
              omitsize=omitsize, encoding=encoding, svgid=svgid, unit=unit,
              svgversion=svgversion, nl=nl)
    return 'data:image/svg+xml{0},{1}' \
                .format(';charset=' + encoding if not omit_charset else '',
                        # Replace " quotes with ' and URL encode the result
                        # See also https://codepen.io/tigt/post/optimizing-svgs-in-data-uris
                        encode(_replace_quotes(buff.getvalue())))


def write_svg_debug(matrix, version, out, scale=15, border=None,
                    fallback_color='fuchsia', color_mapping=None,
                    add_legend=True):  # pragma: no cover
    """\
    Internal SVG serializer which is useful to debugging purposes.

    This function is not exposed to the QRCode class by intention and the
    resulting SVG document is very inefficient (lots of <rect/>s).
    Dark modules are black and light modules are white by default. Provide
    a custom `color_mapping` to override these defaults.
    Unknown modules are red by default.

    :param matrix: The matrix
    :param version: Version constant
    :param out: binary file-like object or file name
    :param scale: Scaling factor
    :param border: Quiet zone
    :param fallback_color: Color which is used for modules which are not 0x0 or 0x1
                and for which no entry in `color_mapping` is defined.
    :param color_mapping: dict of module values to color mapping (optional)
    :param bool add_legend: Indicates if the bit values should be added to the
                matrix (default: True)
    """
    clr_mapping = {
        0x0: '#fff',
        0x1: '#000',
        0x2: 'red',
        0x3: 'orange',
        0x4: 'gold',
        0x5: 'green',
    }
    if color_mapping is not None:
        clr_mapping.update(color_mapping)
    border = get_border(version, border)
    width, height = get_symbol_size(version, scale, border)
    f, must_close = get_writable(out, 'wt', encoding='utf-8')
    legend = []
    write = f.write
    write('<?xml version="1.0" encoding="utf-8"?>\n')
    write('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {0} {1}">'.format(width, height))
    write('<style type="text/css"><![CDATA[ text { font-size: 1px; font-family: Helvetica, Arial, sans; } ]]></style>')
    write('<g transform="scale({0})">'.format(scale))
    for i in range(len(matrix)):
        y = i + border
        for j in range(len(matrix)):
            x = j + border
            bit = matrix[i][j]
            if add_legend and bit not in (0x0, 0x1):
                legend.append((x, y, bit))
            fill = clr_mapping.get(bit, fallback_color)
            write('<rect x="{0}" y="{1}" width="1" height="1" fill="{2}"/>'.format(x, y, fill))
    # legend may be empty if add_legend == False
    for x, y, val in legend:
        write('<text x="{0}" y="{1}">{2}</text>'.format(x+.2, y+.9, val))
    write('</g></svg>\n')
    if must_close:
        f.close()


def write_eps(matrix, version, out, scale=1, border=None, color='#000',
              background=None):
    """\
    Serializes the QR Code as EPS document.

    :param matrix: The matrix to serialize.
    :param int version: The (Micro) QR code version
    :param out: Filename or a file-like object supporting to write strings.
    :param scale: Indicates the size of a single module (default: 1 which
            corresponds to 1 point (1/72 inch) per module).
    :param int border: Integer indicating the size of the quiet zone.
            If set to ``None`` (default), the recommended border size
            will be used (``4`` for QR Codes, ``2`` for a Micro QR Codes).
    :param color: Color of the modules (default: black). The
            color can be provided as ``(R, G, B)`` tuple (this method
            acceppts floats as R, G, B values), as web color name (like
            "red") or in hexadecimal format (``#RGB`` or ``#RRGGBB``).
    :param background: Optional background color (default: ``None`` = no
            background color). See `color` for valid values.
    """
    import textwrap

    def write_line(writemeth, content):
        """\
        Writes `content` and ``LF``.
        """
        # Postscript: Max. 255 characters per line
        for line in textwrap.wrap(content, 254):
            writemeth(line)
            writemeth('\n')

    def rgb_to_floats(clr):
        """\
        Converts the provided color into an acceptable format for Postscript's
         ``setrgbcolor``
        """
        def to_float(c):
            if isinstance(c, float):
                if not 0.0 <= c <= 1.0:
                    raise ValueError('Invalid color "{0}". Not in range 0 .. 1'
                                     .format(c))
                return c
            if not 0 <= c <= 255:
                raise ValueError('Invalid color "{0}". Not in range 0 .. 255'
                                 .format(c))
            return 1/255.0 * c if c != 1 else c

        return tuple([to_float(i) for i in color_to_rgb(clr)])

    check_valid_scale(scale)
    check_valid_border(border)
    f, must_close = get_writable(out, 'wt')
    writeline = partial(write_line, f.write)
    border = get_border(version, border)
    width, height = get_symbol_size(version, scale, border)
    # Write common header
    writeline('%!PS-Adobe-3.0 EPSF-3.0')
    writeline('%%Creator: {0}'.format(CREATOR))
    writeline('%%CreationDate: {0}'.format(time.strftime("%Y-%m-%d %H:%M:%S")))
    writeline('%%DocumentData: Clean7Bit')
    writeline('%%BoundingBox: 0 0 {0} {1}'.format(width, height))
    # Write the shortcuts
    writeline('/m { rmoveto } bind def')
    writeline('/l { rlineto } bind def')
    stroke_color_is_black = color_is_black(color)
    stroke_color = color if stroke_color_is_black else rgb_to_floats(color)
    if background is not None:
        writeline('{0:f} {1:f} {2:f} setrgbcolor clippath fill'
                  .format(*rgb_to_floats(background)))
        if stroke_color_is_black:
            # Reset RGB color back to black iff stroke color is black
            # In case stroke color != black set the RGB color later
            writeline('0 0 0 setrgbcolor')
    if not stroke_color_is_black:
        writeline('{0:f} {1:f} {2:f} setrgbcolor'.format(*stroke_color))
    if scale != 1:
        writeline('{0} {0} scale'.format(scale))
    writeline('newpath')
    # Current pen position y-axis
    # Note: 0, 0 = lower left corner in PS coordinate system
    y = get_symbol_size(version, scale=1, border=0)[1] + border - .5  # .5 = linewidth / 2
    line_iter = matrix_to_lines(matrix, border, y, incby=-1)
    # EPS supports absolute coordinates as well, but relative coordinates
    # are more compact and IMO nicer; so the 1st coordinate is absolute, all
    # other coordinates are relative
    (x1, y1), (x2, y2) = next(line_iter)
    coord = ['{0} {1} moveto {2} 0 l'.format(x1, y1, x2 - x1)]
    append_coord = coord.append
    x = x2
    for (x1, y1), (x2, y2) in line_iter:
        append_coord(' {0} {1} m {2} 0 l'.format(x1 - x, int(y1 - y), x2 - x1))
        x, y = x2, y2
    writeline(''.join(coord))
    writeline('stroke')
    writeline('%%EOF')
    if must_close:
        f.close()


def write_png(matrix, version, out, scale=1, border=None, color='#000',
              background='#fff', compresslevel=9, addad=True):
    """\
    Serializes the QR Code as PNG image.

    By default, the generated PNG will be a greyscale image with a bitdepth
    of 1. If different colors are provided, an indexed-color image with
    the same bitdepth is generated.

    :param matrix: The matrix to serialize.
    :param int version: The (Micro) QR code version
    :param out: Filename or a file-like object supporting to write bytes.
    :param scale: Indicates the size of a single module (default: 1 which
            corresponds to 1 x 1 pixel per module).
    :param int border: Integer indicating the size of the quiet zone.
            If set to ``None`` (default), the recommended border size
            will be used (``4`` for QR Codes, ``2`` for a Micro QR Codes).
    :param color: Color of the modules (default: black). The
            color can be provided as ``(R, G, B)`` tuple, as web color name
            (like "red") or in hexadecimal format (``#RGB`` or ``#RRGGBB``).
    :param background: Optional background color (default: white).
            See `color` for valid values. In addition, ``None`` is
            accepted which indicates a transparent background.
    :param int compresslevel: Integer indicating the compression level
            (default: 9). 1 is fastest and produces the least
            compression, 9 is slowest and produces the most.
            0 is no compression.
    """

    def png_color(clr):
        return color_to_rgb_or_rgba(clr, alpha_float=False)

    def chunk(name, data):
        """\
        Returns a PNG chunk with checksum.
        """
        chunk_head = name + data
        return pack(b'>I', len(data)) + chunk_head \
               + pack(b'>I', zlib.crc32(chunk_head) & 0xFFFFFFFF)

    def groups_of_eight(row):
        """\
        Returns 8 columns from the iterable. If the iterable is of uneven
        length, missing values will be filled-up with ``0x0``.
        """
        return zip_longest(*[iter(row)] * 8, fillvalue=0x0)

    def scale_row_x_axis(row):
        """\
        Returns each pixel `scale` times.
        """
        for b in row:
            for i in range(scale):
                yield b

    def scanline(row):
        """\
        Returns a single scanline.
        """
        return bytearray(chain(b'\0',  # No filter
                               # Pack 8 px into one byte
                               (reduce(lambda x, y: (x << 1) + y, e) for e in groups_of_eight(row))))

    def invert_row_bits(row):
        """\
        Inverts the row bits 0 -> 1, 1 -> 0
        """
        return (b ^ 0x1 for b in row)

    scale = int(scale)
    check_valid_scale(scale)
    check_valid_border(border)
    # Background color index
    bg_color_idx = 0
    trans_color = 1  # white
    stroke_is_transparent, bg_is_transparent = color is None, background is None
    stroke_color = png_color(color) if not stroke_is_transparent else None
    bg_color = png_color(background) if not bg_is_transparent else None
    if stroke_color == bg_color:
        raise ValueError('The stroke color and background color must not be the same')
    stroke_is_black, stroke_is_white = False, False
    bg_is_white, bg_is_black = False, False
    if not stroke_is_transparent:
        stroke_is_black = color_is_black(stroke_color)
        if not stroke_is_black:
            stroke_is_white = color_is_white(stroke_color)
    if not bg_is_transparent:
        bg_is_white = color_is_white(bg_color)
        if not bg_is_white:
            bg_is_black = color_is_black(bg_color)
    transparency = stroke_is_transparent or bg_is_transparent
    is_greyscale = False
    invert_row = False
    if bg_is_white:
        is_greyscale = stroke_is_black or stroke_is_transparent
        invert_row = is_greyscale
        trans_color = int(not is_greyscale)
    elif bg_is_black:
        is_greyscale = stroke_is_transparent or stroke_is_white
    elif bg_is_transparent:
        is_greyscale = stroke_is_black or stroke_is_white
        invert_row = is_greyscale
    palette = None
    if not is_greyscale:
        # PLTE image
        if bg_is_transparent:
            if len(stroke_color) == 3:
                bg_color = invert_color(stroke_color)
            else:
                bg_color = invert_color(stroke_color[:3])
                bg_color += (0,)
        elif stroke_is_transparent:
            if len(bg_color) == 3:
                stroke_color = invert_color(bg_color)
            else:
                stroke_color = invert_color(bg_color[:3])
                stroke_color += (0,)
        palette = sorted([bg_color, stroke_color], key=len, reverse=True)
        bg_color_idx = palette.index(bg_color)
        # Usually, the background color is the first entry in the PLTE so
        # no bit inverting should be necessary
        invert_row = bg_color_idx > 0
    border = get_border(version, border)
    width, height = get_symbol_size(version, scale, border)
    f, must_close = get_writable(out, 'wb')
    write = f.write
    # PNG writing by "hand" since this lib should not rely on PIL/Pillow
    # and PyPNG does not support PNG filters which leads to a suboptimal
    # performance (and file size) if the PNG image should be scaled.
    # I.e. a (unrealistic) scaling factor of 600 would require a 17400 x 17400
    # matrix as input for PyPNG for a 21 x 21 QR Code (+ border = 4) while
    # this algorithm works upon the primary 21 x 21 matrix.
    write(b'\211PNG\r\n\032\n')  # Magic number
    colortype = 3 if not is_greyscale else 0
    if is_greyscale:
        bg_color_idx = int(invert_row)
    # Header:
    # width, height, bitdepth, colortype, compression meth., filter, interlance
    write(chunk(b'IHDR', pack(b'>2I5B', width, height, 1, colortype, 0, 0, 0)))
    if colortype == 3:  # Palette
        write(chunk(b'PLTE', b''.join(pack(b'>3B', *clr[:3]) for clr in palette)))
        # <http://www.w3.org/TR/PNG/#11tRNS>
        if len(palette[0]) > 3:  # Color with alpha is the first in the palette
            f.write(chunk(b'tRNS', b''.join(pack(b'>B', clr[3]) for clr in palette if len(clr) > 3)))
        elif transparency:
            f.write(chunk(b'tRNS', pack(b'>B', bg_color_idx)))
    elif is_greyscale and transparency:  # Greyscale with alpha
        # Greyscale with alpha channel
        # <http://www.w3.org/TR/PNG/#11tRNS>
        # 2 bytes for color type == 0 (greyscale)
        write(chunk(b'tRNS', pack(b'>1H', trans_color)))  # 1 == "white"
    horizontal_border, vertical_border = b'', b''
    if border > 0:
        # Calculate horizontal and vertical border
        horizontal_border = scanline([bg_color_idx] * width) * border * scale
        vertical_border = [bg_color_idx] * border * scale
    # <http://www.w3.org/TR/PNG/#9Filters>
    # This variable holds the "Up" filter which indicates that this scanline
    # is equal to the above scanline (since it is filled with null bytes)
    same_as_above = b''
    row_filters = []
    if invert_row:
        row_filters.append(invert_row_bits)
    if scale > 1:
        # 2 == PNG Filter "Up"
        # width / 8 = Filters work on bytes, not pixels
        # <https://www.w3.org/TR/PNG/#9-table91>
        same_as_above = bytearray((b'\2' + b'\0' * int(math.ceil(width / 8)))) * (scale - 1)
        row_filters.append(scale_row_x_axis)
    res = bytearray(horizontal_border)
    for row in matrix:
        row = reduce(lambda r, fn: fn(r), row_filters, row)
        # Chain precalculated left border with row and right border
        res += scanline(chain(vertical_border, row, vertical_border))
        res += same_as_above  # This is b'' if no scaling factor was provided
    res += horizontal_border
    if _PY2:
        res = bytes(res)
    write(chunk(b'IDAT', zlib.compress(res, compresslevel)))
    if addad:
        write(chunk(b'tEXt', b'Software\x00' + CREATOR.encode('ascii')))
    write(chunk(b'IEND', b''))
    if must_close:
        f.close()


def as_png_data_uri(matrix, version, scale=1, border=None, color='#000',
                    background='#fff', compresslevel=9, addad=True):
    """\
    Converts the provided matrix into a PNG data URI.

    :rtype: str
    """
    buff = io.BytesIO()
    write_png(matrix, version, buff, scale=scale, border=border, color=color,
              background=background, compresslevel=compresslevel, addad=addad)
    return 'data:image/png;base64,{0}' \
                .format(base64.b64encode(buff.getvalue()).decode('ascii'))


def write_pdf(matrix, version, out, scale=1, border=None, compresslevel=9):
    """\
    Serializes the QR Code as PDF document.

    :param matrix: The matrix to serialize.
    :param int version: The (Micro) QR code version
    :param out: Filename or a file-like object supporting to write bytes.
    :param scale: Indicates the size of a single module (default: 1 which
            corresponds to 1 x 1 pixel per module).
    :param int border: Integer indicating the size of the quiet zone.
            If set to ``None`` (default), the recommended border size
            will be used (``4`` for QR Codes, ``2`` for a Micro QR Codes).
    :param int compresslevel: Integer indicating the compression level
            (default: 9). 1 is fastest and produces the least
            compression, 9 is slowest and produces the most.
            0 is no compression.
    """

    def write_string(writemeth, s):
        writemeth(s.encode('ascii'))

    check_valid_scale(scale)
    check_valid_border(border)
    f, must_close = get_writable(out, 'wb')
    width, height = get_symbol_size(version, scale, border)
    border = get_border(version, border)
    creation_date = "{0}{1:+03d}'{2:02d}'".format(time.strftime('%Y%m%d%H%M%S'),
                                                  time.timezone // 3600,
                                                  abs(time.timezone) % 60)
    cmds = []
    append_cmd = cmds.append
    if scale > 1:
        append_cmd('{0} 0 0 {0} 0 0 cm  '.format(scale))
    # Current pen position y-axis
    # Note: 0, 0 = lower left corner in PDF coordinate system
    y = get_symbol_size(version, scale=1, border=0)[1] + border - .5
    # Set the origin in the upper left corner
    append_cmd('1 0 0 1 {0} {1} cm'.format(border, y))
    # PDF supports absolute coordinates, only
    for (x1, y1), (x2, y2) in matrix_to_lines(matrix, 0, 0, incby=-1):
        append_cmd(' {0} {1} m {2} {1} l'.format(x1, y1, x2, y2))
    append_cmd(' S')
    graphic = zlib.compress((''.join(cmds)).encode('ascii'), compresslevel)
    write = f.write
    writestr = partial(write_string, write)
    object_pos = []
    write(b'%PDF-1.4\r%\xE2\xE3\xCF\xD3\r\n')
    for obj in ('obj <</Type /Catalog /Pages 2 0 R>>\r\nendobj\r\n',
                'obj <</Type /Pages /Kids [3 0 R] /Count 1>>\r\nendobj\r\n',
                'obj <</Type /Page /Parent 2 0 R /MediaBox [0 0 {0} {1}] /Contents 4 0 R>>\r\nendobj\r\n'.format(width, height),
                'obj <</Length {0} /Filter /FlateDecode>>\r\nstream\r\n'.format(len(graphic))):
        object_pos.append(f.tell())
        writestr('{0} 0 {1}'.format(len(object_pos), obj))
    write(graphic)
    write(b'\r\nendstream\r\nendobj\r\n')
    object_pos.append(f.tell())
    writestr('{0} 0 obj <</CreationDate(D:{1})/Producer({2})/Creator({2})\r\n>>\r\nendofbj\r\n' \
             .format(len(object_pos), creation_date, CREATOR))
    object_pos.append(f.tell())
    xref_location = f.tell()
    writestr('xref\r\n0 {0}\r\n0000000000 65535 f\r\n'.format(len(object_pos) + 1))
    for pos in object_pos:
        writestr('{0:010d} {1:05d} n\r\n'.format(pos, 0))
    writestr('trailer <</Size {0}/Root 1 0 R/Info 5 0 R>>\r\n'.format(len(object_pos) + 1))
    writestr('startxref\r\n{0}\r\n%%EOF\r\n'.format(xref_location))
    if must_close:
        f.close()


def write_txt(matrix, version, out, border=None, color='1', background='0'):
    """\
    Serializes QR code in a text format.

    :param matrix: The matrix to serialize.
    :param int version: The (Micro) QR code version
    :param out: Filename or a file-like object supporting to write text.
    :param int border: Integer indicating the size of the quiet zone.
            If set to ``None`` (default), the recommended border size
            will be used (``4`` for QR Codes, ``2`` for a Micro QR Codes).
    :param color: Character to use for the black modules (default: '1')
    :param background: Character to use for the white modules (default: '0')
    """
    row_iter = matrix_iter(matrix, version, scale=1, border=border)
    colors = (str(background), str(color))
    f, must_close = get_writable(out, 'wt')
    write = f.write
    for row in row_iter:
        write(''.join([colors[i] for i in row]))
        write('\n')
    if must_close:
        f.close()


def write_pbm(matrix, version, out, scale=1, border=None, plain=False):
    """\
    Serializes the matrix in PBM format.

    :param matrix: The matrix to serialize.
    :param int version: The (Micro) QR code version
    :param out: Filename or a file-like object supporting to write binary data.
    :param scale: Indicates the size of a single module (default: 1 which
            corresponds to 1 x 1 pixel per module).
    :param int border: Integer indicating the size of the quiet zone.
            If set to ``None`` (default), the recommended border size
            will be used (``4`` for QR Codes, ``2`` for a Micro QR Codes).
    :param bool plain: Indicates if a P1 image should be created (default: False).
            By default a P4 image is created.
    """
    def groups_of_eight(row):
        """\
        Returns 8 columns from the iterable. If the iterable is of uneven
        length, missing values will be filled-up with ``0x0``.
        """
        return zip_longest(*[iter(row)] * 8, fillvalue=0x0)

    width, height = get_symbol_size(version, scale=scale, border=border)
    f, must_close = get_writable(out, 'wb')
    write = f.write
    kind = b'P4' if not plain else b'P1'
    write(kind + '\n# Created by {0}\n{1} {2}\n' \
          .format(CREATOR, width, height).encode('ascii'))
    row_iter = matrix_iter(matrix, version, scale, border)
    if not plain:
        for row in row_iter:
            write(bytearray(reduce(lambda x, y: (x << 1) + y, e) for e in groups_of_eight(row)))
    else:
        for row in row_iter:
            write(b''.join(str(i).encode('ascii') for i in row))
            write(b'\n')
    if must_close:
        f.close()


def write_tex(matrix, version, out, scale=1, border=None, unit='pt', url=None):
    """\
    Serializes the matrix as LaTeX PGF picture.

    Requires the `PGF/TikZ <https://en.wikipedia.org/wiki/PGF/TikZ>`_ package
    (i.e. ``\\usepackage{pgf}``) in the LaTeX source.

    :param matrix: The matrix to serialize.
    :param int version: The (Micro) QR code version
    :param out: Filename or a file-like object supporting to write text data.
    :param scale: Indicates the size of a single module (default: 1 which
            corresponds to 1 x 1 in the provided unit per module).
    :param int border: Integer indicating the size of the quiet zone.
            If set to ``None`` (default), the recommended border size
            will be used (``4`` for QR Codes, ``2`` for a Micro QR Codes).
    :param unit: Unit of the drawing (default: ``pt``)
    :param url: Optional URL where the QR Code should point to. Requires the
            "hyperref" package. Default: ``None``.
    """
    def point(x, y):
        return '\pgfqpoint{{{0}{2}}}{{{1}{2}}}'.format(x, y, unit)

    check_valid_scale(scale)
    check_valid_border(border)
    border = get_border(version, border)
    f, must_close = get_writable(out, 'wt')
    write = f.write
    write('%% Creator:  {0}\n'.format(CREATOR))
    write('%% Date:     {0}\n'.format(time.strftime('%Y-%m-%dT%H:%M:%S')))
    if url:
        write('\href{{{0}}}{{\n'.format(url))
    write('\\begin{pgfpicture}\n')
    write('  \pgfsetlinewidth{{{0}{1}}}\n'.format(scale, unit))
    x, y = border, -border
    for (x1, y1), (x2, y2) in matrix_to_lines(matrix, x, y, incby=-1):
        write('  \pgfpathmoveto{{{0}}}\n'.format(point(x1 * scale, y1 * scale)))
        write('  \pgfpathlineto{{{0}}}\n'.format(point(x2 * scale, y2 * scale)))
    write('  \pgfusepath{stroke}\n')
    write('\end{{pgfpicture}}{0}\n'.format('' if not url else '}'))
    if must_close:
        f.close()


def write_terminal(matrix, version, out, border=None):
    """\
    Function to write to a terminal which supports ANSI escape codes.

    :param matrix: The matrix to serialize.
    :param int version: The (Micro) QR code version.
    :param out: Filename or a file-like object supporting to write text.
    :param int border: Integer indicating the size of the quiet zone.
            If set to ``None`` (default), the recommended border size
            will be used (``4`` for QR Codes, ``2`` for a Micro QR Codes).
    """
    f, must_close = get_writable(out, 'wt')
    write = f.write
    colors = ['\033[{0}m'.format(i) for i in (7, 49)]
    for row in matrix_iter(matrix, version, scale=1, border=border):
        prev_bit = -1
        cnt = 0
        for bit in row:
            if bit == prev_bit:
                cnt += 1
            else:
                if cnt:
                    write(colors[prev_bit])
                    write('  ' * cnt)
                    write('\033[0m')  # reset color
                prev_bit = bit
                cnt = 1
        if cnt:
            write(colors[prev_bit])
            write('  ' * cnt)
            write('\033[0m')  # reset color
        write('\n')
    if must_close:
        f.close()


def write_terminal_win(matrix, version, border=None):  # pragma: no cover
    """\
    Function to write a QR Code to a MS Windows terminal.

    :param matrix: The matrix to serialize.
    :param int version: The (Micro) QR code version
    :param int border: Integer indicating the size of the quiet zone.
            If set to ``None`` (default), the recommended border size
            will be used (``4`` for QR Codes, ``2`` for a Micro QR Codes).
    """
    import sys
    import struct
    import ctypes
    write = sys.stdout.write
    std_out = ctypes.windll.kernel32.GetStdHandle(-11)
    csbi = ctypes.create_string_buffer(22)
    res = ctypes.windll.kernel32.GetConsoleScreenBufferInfo(std_out, csbi)
    if not res:
        raise OSError('Cannot find information about the console. '
                      'Not running on the command line?')
    default_color = struct.unpack(b'hhhhHhhhhhh', csbi.raw)[4]
    set_color = partial(ctypes.windll.kernel32.SetConsoleTextAttribute, std_out)
    colors = (240, default_color)
    for row in matrix_iter(matrix, version, scale=1, border=border):
        prev_bit = -1
        cnt = 0
        for bit in row:
            if bit == prev_bit:
                cnt += 1
            else:
                if cnt:
                    set_color(colors[prev_bit])
                    write('  ' * cnt)
                prev_bit = bit
                cnt = 1
        if cnt:
            set_color(colors[prev_bit])
            write('  ' * cnt)
        set_color(default_color)  # reset color
        write('\n')


_VALID_SERIALISERS = {
    'svg': write_svg,
    'svg_debug': write_svg_debug,
    'png': write_png,
    'eps': write_eps,
    'txt': write_txt,
    'pdf': write_pdf,
    'ans': write_terminal,
    'pbm': write_pbm,
    'tex': write_tex,
}

def save(matrix, version, out, kind=None, **kw):
    """\
    Serializes the matrix in any of the supported formats.

    :param matrix: The matrix to serialize.
    :param int version: The (Micro) QR code version
    :param out: A filename or a writable file-like object with a
            ``name`` attribute. If a stream like :py:class:`io.ByteIO` or
            :py:class:`io.StringIO` object without a ``name`` attribute is
            provided, use the `kind` parameter to specify the serialization
            format.
    :param kind: If the desired output format cannot be extracted from
            the filename, this parameter can be used to indicate the
            serialization format (i.e. "svg" to enforce SVG output)
    :param kw: Any of the supported keywords by the specific serialization
            method.
    """
    is_stream = False
    if kind is None:
        try:
            fname = out.name
            is_stream = True
        except AttributeError:
            fname = out
        ext = fname[fname.rfind('.') + 1:].lower()
    else:
        ext = kind.lower()
    if not is_stream and ext == 'svgz':
        f = gzip.open(out, 'wb', compresslevel=kw.pop('compresslevel', 9))
        try:
            _VALID_SERIALISERS['svg'](matrix, version, f, **kw)
        finally:
            f.close()
    else:
        if kw.pop('debug', False) and ext == 'svg':
            ext = 'svg_debug'
        try:
            _VALID_SERIALISERS[ext](matrix, version, out, **kw)
        except KeyError:
            raise ValueError('Unknown file extension ".{0}"'.format(ext))

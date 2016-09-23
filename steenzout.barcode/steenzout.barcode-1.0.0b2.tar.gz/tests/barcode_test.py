# -*- coding: utf-8 -*-
"""Performs some tests with pyBarcode.

All created bar codes are saved in the tests subdirectory.

You can use the index.html to watch them."""

import sys
import os


import codecs

from steenzout import barcode
from steenzout.barcode import factory


try:
    from steenzout.barcode.writer import ImageWriter
except ImportError:
    ImageWriter = None  # lint:ok


__docformat__ = 'restructuredtext en'

PATH = os.path.dirname(os.path.abspath(__file__))
TESTPATH = os.path.join(PATH, '.')
HTMLFILE = os.path.join(TESTPATH, 'index.html')

HTML = """<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN"
    "http://www.w3.org/TR/html4/strict.dtd">
<html>
    <head>
        <title>barcode {version} tests</title>
        <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
    </head>
    <body>
        <h1>barcode {version} tests</h1>
        {body}
    </body>
</html>
"""

OBJECTS = ('<p><h2>{name}</h2><br />\n'
           '<object data="{filename}" type="image/svg+xml">\n'
           '<param name="src" value="{filename}" /></object>')

IMAGES = ('<h3>As PNG-Image</h3><br />\n'
          '<img src="{filename}" alt="{name}" /></p>\n')

NO_PIL = '<h3>PIL was not found. No PNG-Image created.</h3></p>\n'

TESTCODES = (
    ('ean8', '40267708'),
    ('ean13', '5901234123457'),
    ('upca', '360002914539'),
    ('jan', '4901234567894'),
    ('isbn10', '3-12-517154-7'),
    ('isbn13', '978-3-16-148410-0'),
    ('issn', '1144875X'),
    ('code39', 'Example Code 39'),
    ('pzn', '487780'),
    ('code128', 'Example Code 128 998866'),
)


def test():
    if not os.path.isdir(TESTPATH):
        try:
            os.mkdir(TESTPATH)
        except OSError as e:
            print('Test not run.')
            print('Error:', e)
            sys.exit(1)
    objects = []

    def append(x, y):
        objects.append(OBJECTS.format(filename=x, name=y))

    def append_img(x, y):
        objects.append(IMAGES.format(filename=x, name=y))

    options = dict(module_width=0.495, module_height=25.0)
    for codename, code in TESTCODES:
        bar_code = factory.create_instance(codename, code)
        if codename.startswith('i'):
            options['center_text'] = False
        else:
            options['center_text'] = True
        filename = bar_code.save(os.path.join(TESTPATH, codename), options)
        print('Code: %s, Input: %s, Output: %s' % (bar_code.name, code, bar_code.get_fullcode()))

        append(filename, bar_code.name)
        if ImageWriter is not None:
            bar_code = factory.create_instance(codename, code, writer=ImageWriter())
            opts = dict(font_size=14, text_distance=1)
            if codename.startswith('i'):
                opts['center_text'] = False
            else:
                options['center_text'] = True
            filename = bar_code.save(os.path.join(TESTPATH, codename), opts)
            append_img(filename, bar_code.name)
        else:
            objects.append(NO_PIL)

    # Save htmlfile with all objects
    with codecs.open(HTMLFILE, 'w', encoding='utf-8') as f:
        obj = '\n'.join(objects)
        f.write(HTML.format(version=barcode.__version__, body=obj))

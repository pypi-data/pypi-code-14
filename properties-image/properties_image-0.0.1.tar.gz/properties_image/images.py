"""images.py: Image file property classes"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import base64
from io import BytesIO

import png
import properties
from six import string_types                                                   #pylint: disable=wrong-import-order


PNG_PREAMBLE = 'data:image/png;base64,'


class ImagePNG(properties.Property):
    """Property for PNG images

    Available keyword:

    * **filename** - name associated with open copy of PNG image
      (default is 'texture.png')
    """
    info_text = 'a PNG image file'

    @property
    def filename(self):
        """Bytestream image filename"""
        return getattr(self, '_filename', 'texture.png')

    @filename.setter
    def filename(self, value):
        if not isinstance(value, string_types):
            raise TypeError('Filename must be a string')
        self._filename = value

    def validate(self, obj, value):
        """Checks that the value is an open PNG file or valid PNG filename

        Returns an open bytestream of the image
        """
        if getattr(value, '__valid__', False):
            return value

        if hasattr(value, 'read'):
            try:
                png.Reader(value).validate_signature()
            except png.FormatError:
                self.error(obj, value, extra='Open file is not PNG.')
            value.seek(0)
        elif isinstance(value, string_types):
            try:
                val = open(value, 'rb')
            except IOError:
                self.error(obj, value, extra='Invalid file name.')
            try:
                png.Reader(val).validate_signature()
            except png.FormatError:
                self.error(obj, value, extra='File is not PNG.')
            val.close()
        else:
            self.error(obj, value)

        output = BytesIO()
        output.name = self.filename
        output.__valid__ = True
        if hasattr(value, 'read'):
            fid = value
            fid.seek(0)
        else:
            fid = open(value, 'rb')
        output.write(fid.read())
        output.seek(0)
        fid.close()
        return output

    @staticmethod
    def to_json(value):
        """Convert a PNG Image to base64-encoded JSON

        to_json assumes that value has passed validation.
        """
        b64rep = base64.b64encode(value.read())
        value.seek(0)
        jsonrep = '{preamble}{b64}'.format(
            preamble=PNG_PREAMBLE,
            b64=b64rep.decode(),
        )
        return jsonrep

    @staticmethod
    def from_json(value):
        """Convert a PNG Image from base64-encoded JSON"""
        if not value.startswith(PNG_PREAMBLE):
            raise ValueError('Not a valid base64-encoded PNG image')
        infile = BytesIO()
        rep = base64.b64decode(value[len(PNG_PREAMBLE):].encode('utf-8'))
        infile.write(rep)
        infile.seek(0)
        return infile

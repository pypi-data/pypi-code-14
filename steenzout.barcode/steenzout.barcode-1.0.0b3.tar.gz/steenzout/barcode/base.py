# -*- coding: utf-8 -*-
"""Base bar code module."""

from abc import abstractmethod, ABCMeta

from steenzout.object import Object

from . import writer


class Barcode(Object):
    """Base bar code class."""

    __metaclass__ = ABCMeta

    name = ''

    raw = None

    digits = 0

    def __init__(self, code, writer=None):
        self.code = code
        self.writer = writer

    def __repr__(self):
        """Returns the canonical string representation of the object.

        Returns:
            (str): the canonical string representation of the object.
        """
        return '<{0}({1!r})>'.format(
            self.__class__.__name__, self.get_fullcode()
        )

    def __unicode__(self):
        if isinstance(self.code, unicode):
            return self.code
        else:
            unicode(self.code)

    __str__ = __unicode__

    @classmethod
    @abstractmethod
    def calculate_checksum(cls, code):
        """Calculates a bar code checksum.

        Args:
            code (str): the code.

        Returns:
            (integer): the checksum.
        """
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def validate(cls, code):
        """Validates the given bar code."""
        raise NotImplementedError

    @abstractmethod
    def build(self):
        """

        Returns:
             (str):
        """
        raise NotImplementedError

    @property
    def checksum(self):
        """(int): bar code checksum."""
        return type(self).calculate_checksum(self.code)

    @property
    def code(self):
        """(str): bar code."""
        return self._code

    @code.setter
    def code(self, value):
        type(self).validate(value)
        self._code = value
        self._checksum = type(self).calculate_checksum(value)

    @property
    def writer(self):
        """(:py:class:`steenzout.barcode.writer.Interface`): writer instance."""
        return self._writer

    @writer.setter
    def writer(self, value):
        if value is None:
            self._writer = writer.DEFAULT_WRITER()
        elif isinstance(value, writer.Interface):
            self._writer = value
        else:
            raise ValueError(value)

    @abstractmethod
    def get_fullcode(self):
        """Returns the full code, encoded in the barcode.

        Returns:
            (str): Full human readable code.
        """
        raise NotImplementedError

    def render(self, writer_options=None):
        """Renders the barcode using `self.writer`.

        Args:
            writer_options (dict):
                options for `self.writer`, see writer docs for details.

        Returns:
            output of the writer's render method.
        """
        options = writer.DEFAULT_WRITER_OPTIONS.copy()
        options.update(writer_options or {})

        if 'write_text' in options and options['write_text']:
            options['text'] = self.get_fullcode()

        self.writer.set_options(options)

        code = self.build()

        Barcode.raw = self.writer.render(code)
        return Barcode.raw

    def save(self, filename, options=None):
        """Renders the barcode and saves it in `filename`.

        Args:
            filename (str): filename to save the barcode in (without filename extension).
            options (dict): the same as in `:py:func:`self.render`.

        Returns:
            (str): Filename with extension.
        """
        output = self.render(options)
        _filename = self.writer.save(filename, output)
        return _filename

    def to_ascii(self):
        """Returns ASCII representation of the bar code.

        Returns:
            (str): ASCII representation of the bar code.
        """
        code = self.build()
        for i, line in enumerate(code):
            code[i] = line.replace('1', 'X').replace('0', ' ')
        return '\n'.join(code)

    def write(self, fp, options=None):
        """Renders the barcode and writes it to the file like object `fp`.

        Args:
            fp : File like object
                object to write the raw data in.
            options (dict): the same as in `:py:func:`self.render`.
        """
        output = self.render(options)
        if hasattr(output, 'tostring'):
            output.save(fp, format=self.writer.format)
        else:
            fp.write(output)

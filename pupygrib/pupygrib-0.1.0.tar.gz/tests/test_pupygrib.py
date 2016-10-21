"""Unit and regression tests for pupygrib's public interface."""

from __future__ import unicode_literals

from os import path

import pkg_resources
import pytest
import six

import pupygrib


def open_grib(filename):
    return pkg_resources.resource_stream(__name__, path.join('data', filename))


class TestRead:

    """Unit and regression tests for the read() function."""

    def test_read_empty_file(self):
        with pytest.raises(StopIteration):
            next(pupygrib.read(six.BytesIO()))

    def test_read_not_a_grib(self):
        with pytest.raises(pupygrib.ParseError, message="not a GRIB message"):
            next(pupygrib.read(six.BytesIO(b'GRUB')))

    def test_read_truncated_header(self):
        error_message = "unexpected end of file"
        with pytest.raises(pupygrib.ParseError, message=error_message):
            next(pupygrib.read(six.BytesIO(b'GRIB')))

    def test_read_truncated_edition1_body(self):
        error_message = "unexpected end of file"
        with pytest.raises(pupygrib.ParseError, message=error_message):
            next(pupygrib.read(six.BytesIO(b'GRIB\x00\x00\x09\x01')))

    def test_read_truncated_edition2_body(self):
        error_message = "unexpected end of file"
        data = b'GRIBxxx\x02\x00\x00\x00\x00\x00\x00\x00\x11'
        with pytest.raises(pupygrib.ParseError, message=error_message):
            next(pupygrib.read(six.BytesIO(data)))

    def test_read_without_end_of_message_marker(self):
        error_message = "end-of-message marker not found"
        data = b'GRIB\x00\x00\x0c\x017776'
        with pytest.raises(pupygrib.ParseError, message=error_message):
            next(pupygrib.read(six.BytesIO(data)))

    def test_read_unknown_edition(self):
        error_message = "unknown edition number '3'"
        with pytest.raises(pupygrib.ParseError, message=error_message):
            next(pupygrib.read(six.BytesIO(b'GRIBxxx\x03')))

    def test_read_edition1(self):
        with open_grib('regular_latlon_surface.grib1') as stream:
            msg = next(pupygrib.read(stream))
        assert msg[0].editionNumber == 1

    def test_read_edition2(self):
        with open_grib('regular_latlon_surface.grib2') as stream:
            msg = next(pupygrib.read(stream))
        assert msg[0].editionNumber == 2

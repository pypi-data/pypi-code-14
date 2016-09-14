from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase

from django_gpxpy.gpx_parse import parse_gpx, parse_gpx_filefield


class DjangoGpxPyTests(TestCase):
    def test_gpx_parsing(self):
        """
        test if the admin page with RelatedFieldRadioFilter filters loads succesfully
        """
        with open("tests/test_data/test_track.gpx", "r") as f:
            multilinestring = parse_gpx(f)
        self.assertEquals(multilinestring.num_geom, 26)
        self.assertEquals(multilinestring.length, 0.31341761110953986)

    def test_gpx_parse_filefiled(self):
        """
        test if the admin page with RelatedFieldRadioFilter filters loads succesfully
        """
        with open("tests/test_data/test_track.gpx", "rb") as f:
            file_field = SimpleUploadedFile('tests/test_data/test_track.gpx', f.read())
            multilinestring = parse_gpx_filefield(file_field)
        self.assertEquals(multilinestring.num_geom, 26)
        self.assertEquals(multilinestring.length, 0.31341761110953986)

    def test_gpx_parse_filefiled_gz(self):
        """
        test if the admin page with RelatedFieldRadioFilter filters loads succesfully
        """
        with open("tests/test_data/test_track.gpx.gz", "rb") as f:
            file_field = SimpleUploadedFile('tests/test_data/test_track.gpx.gz', f.read())
            multilinestring = parse_gpx_filefield(file_field)
        self.assertEquals(multilinestring.num_geom, 26)
        self.assertEquals(multilinestring.length, 0.31341761110953986)

    def test_gpx_with_route(self):
        """
        test if the admin page with RelatedFieldRadioFilter filters loads succesfully
        """
        with open("tests/test_data/test_with_route.gpx", "r") as f:
            multilinestring = parse_gpx(f)
        self.assertEquals(multilinestring.num_geom, 1)
        self.assertEquals(multilinestring.length, 0.10557333372775202)

    def test_bad_file_parsing(self):
        """
        test if the admin page with RelatedFieldRadioFilter filters loads succesfully
        """
        with self.assertRaises(ValidationError):
            with open("tests/test_data/test_bad_file.gpx", "r") as f:
                parse_gpx(f)

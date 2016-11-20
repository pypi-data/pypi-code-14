# coding=utf-8
from mock import patch

from django.core.exceptions import ValidationError
from django.test.testcases import TestCase

from stdnumfield.validators import StdnumFormatValidator


class ValidatorsTests(TestCase):

    def test_invalid_format(self):
        validator = StdnumFormatValidator(formats=['damn'])
        self.assertRaisesMessage(
            ValueError,
            'Unknown stdnum format: "damn"',
            validator,
            '123456',
        )

    def test_valid_format_valid_value(self):
        validator = StdnumFormatValidator(formats=['hr.oib'])
        validator('69435151530')

    def test_valid_format_invalid_value(self):
        validator = StdnumFormatValidator(formats=['hr.oib'])
        self.assertRaises(
            ValidationError,
            validator,
            '69435151531',
        )

    def test_default_format_valid_value(self):
        validator = StdnumFormatValidator(formats=['hr.oib'])
        validator('69435151530')

    @patch('stdnumfield.settings.DEFAULT_FORMATS', [])
    def test_empty_format(self):
        validator = StdnumFormatValidator(formats=None)
        self.assertRaisesMessage(
            ValueError,
            'StdnumFormatValidator called without specified formats',
            validator,
            '69435151530',
        )

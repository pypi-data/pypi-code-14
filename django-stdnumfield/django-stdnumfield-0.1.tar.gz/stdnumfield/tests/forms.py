# coding=utf-8
from mock import patch

from django.test import TestCase

from stdnumfield.forms import StdnumField


VALID_OIB = '69435151530'
INVALID_OIB = '69435151531'


class FormFieldInitTest(TestCase):

    def test_single_format(self):
        try:
            StdnumField(formats='hr.oib')
        except Exception as e:
            self.assertIsNone(e)

    def test_multiple_formats(self):
        try:
            StdnumField(formats=['hr.oib', 'damm'])
        except Exception as e:
            self.assertIsNone(e)

    def test_invalid_single_formats(self):
        self.assertRaisesMessage(
            ValueError,
            'Unknown format for StdnumField',
            StdnumField,
            formats='damn',
        )

    def test_invalid_in_list_formats(self):
        self.assertRaisesMessage(
            ValueError,
            'Unknown format for StdnumField',
            StdnumField,
            formats=['damm', 'damn'],
        )

    def test_no_formats(self):
        self.assertRaisesMessage(
            ValueError,
            'StdnumField defined without formats',
            StdnumField,
        )


class FormFieldValidateTest(TestCase):
    formats = ['hr.oib']

    @patch('stdnumfield.forms.StdnumFormatValidator')
    def test_validate(self, validator_class):
        field = StdnumField(formats=self.formats)
        field.validate(VALID_OIB)
        validator_class.assert_called_once_with(self.formats)
        validator_instance = validator_class.return_value
        validator_instance.assert_called_once_with(VALID_OIB)

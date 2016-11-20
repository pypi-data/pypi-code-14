# coding=utf-8
from django.test.testcases import TestCase

from stdnumfield.models import StdNumField
from stdnumfield.testproject.testapp.models import SomeModel
from .forms import VALID_OIB


class ModelFieldTests(TestCase):

    def setUp(self):
        self.instance = SomeModel()

    def test_save(self):
        self.instance.oib = VALID_OIB
        self.instance.save()
        instance = SomeModel.objects.first()
        self.assertEqual(instance.oib, VALID_OIB)

    def test_save2(self):
        self.instance.oib = VALID_OIB
        self.instance.save()
        instance = SomeModel.objects.first()
        self.assertEqual(instance.oib, VALID_OIB)

    def test_max_length_passed_to_formfield(self):
        """
        CharField passes its max_length attribute to form fields created using
        the formfield() method.
        """
        field = StdNumField('hr.oib')
        self.assertEqual(254, field.formfield().max_length)

# -*- coding: utf-8 -*-
from django.test import TestCase
from djmessenger.models import *
from djmessenger.exceptions import DJMInvalidConfigException
from djmessenger.settings import *


class TestGreetings(TestCase):
    def test_basic(self):
        try:
            gr = Greetings(text='Welcome to the page')
            gr.save()
        except Exception as e:
            self.fail('Should not fail but fail because %s' % e)

    def test_add_second_should_fail(self):
        try:
            gr = Greetings(text='Welcome to the page')
            gr.save()
        except Exception as e:
            self.fail('Should not fail but fail because %s' % e)
        with self.assertRaises(DJMInvalidConfigException):
            Greetings.objects.create(text='This is the second greetings')

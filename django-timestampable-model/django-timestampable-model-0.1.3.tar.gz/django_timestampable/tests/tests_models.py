# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function

import time
from django.test import TestCase
from django_timestampable.models import TimestampableModel


class DemoTimestampableModel(TimestampableModel):
    pass


class TimestampableModelMixinTestCase(TestCase):
    """
    Test the TimestampableModel Mixin !
    """

    def test_created_at_after_save(self):
        new_instance = DemoTimestampableModel()
        self.assertIsNone(new_instance.created_at)
        new_instance.save()
        self.assertIsNotNone(new_instance.created_at)

    def test_update_at_after_update(self):
        new_instance = DemoTimestampableModel.objects.create()
        tmp_updated_at = new_instance.updated_at
        self.assertIsNotNone(new_instance.updated_at)
        time.sleep(2)
        new_instance.save()
        self.assertNotEqual(tmp_updated_at,
                            new_instance.updated_at)


# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations


def forwards_func(apps, schema_editor):
    pass


def reverse_func(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('tests', '0003_unshardedtestmodel_more_random_string'),
    ]

    operations = [
        migrations.RunPython(forwards_func, reverse_func, hints={"model_name": "tests.TestModel"}),
    ]

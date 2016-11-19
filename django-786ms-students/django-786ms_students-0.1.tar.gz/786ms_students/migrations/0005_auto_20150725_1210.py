# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0004_auto_20150725_1040'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='applied_before',
            field=models.TextField(max_length=3, choices=[(b'yes', b'yes'), (b'no', b'no')]),
        ),
        migrations.AlterField(
            model_name='studenttoken',
            name='token',
            field=models.CharField(default=b'71295033', unique=True, max_length=8, editable=False),
        ),
    ]

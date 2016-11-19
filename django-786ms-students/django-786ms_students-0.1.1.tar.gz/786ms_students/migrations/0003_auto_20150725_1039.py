# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('786ms_students', '0002_auto_20150725_0950'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='CCCUser',
            new_name='Student',
        ),
        migrations.AlterField(
            model_name='studenttoken',
            name='token',
            field=models.CharField(default=b'7c893370', unique=True, max_length=8, editable=False),
        ),
    ]

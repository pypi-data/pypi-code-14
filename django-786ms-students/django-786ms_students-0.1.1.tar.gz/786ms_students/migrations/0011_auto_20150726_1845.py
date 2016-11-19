# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('786ms_students', '0010_auto_20150726_1826'),
    ]

    operations = [
        migrations.RenameField(
            model_name='student',
            old_name='interested_in',
            new_name='courses',
        ),
        migrations.AlterField(
            model_name='studenttoken',
            name='token',
            field=models.CharField(default=b'01c518db', unique=True, max_length=8, editable=False),
        ),
    ]

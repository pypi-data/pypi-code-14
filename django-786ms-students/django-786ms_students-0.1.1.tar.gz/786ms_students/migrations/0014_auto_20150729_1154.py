# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('786ms_students', '0013_auto_20150729_0007'),
    ]

    operations = [
        migrations.AddField(
            model_name='studenttoken',
            name='datetime',
            field=models.DateTimeField(default=datetime.datetime.now, editable=False),
        ),
        migrations.AlterField(
            model_name='studenttoken',
            name='token',
            field=models.CharField(default=b'81EB4A68', unique=True, max_length=8, editable=False),
        ),
    ]

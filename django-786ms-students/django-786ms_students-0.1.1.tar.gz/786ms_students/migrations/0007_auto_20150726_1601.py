# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('786ms_students', '0006_auto_20150726_1541'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='studenttoken',
            name='date_of_birth',
        ),
        migrations.AddField(
            model_name='studenttoken',
            name='email',
            field=models.EmailField(default='a@a.a', max_length=254),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='studenttoken',
            name='token',
            field=models.CharField(default=b'211ee796', unique=True, max_length=8, editable=False),
        ),
    ]

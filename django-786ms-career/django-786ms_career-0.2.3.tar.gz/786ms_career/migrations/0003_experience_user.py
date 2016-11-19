# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('786ms_career', '0002_experience'),
    ]

    operations = [
        migrations.AddField(
            model_name='experience',
            name='user',
            field=models.ForeignKey(default=1, to='786ms_career.User'),
            preserve_default=False,
        ),
    ]

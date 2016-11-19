# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('786ms_career', '0003_experience_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='qualification',
            name='marks',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]

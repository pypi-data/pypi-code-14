# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('786ms_career', '0004_qualification_marks'),
    ]

    operations = [
        migrations.AlterField(
            model_name='qualification',
            name='marks',
            field=models.FloatField(),
        ),
    ]

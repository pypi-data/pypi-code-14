# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('786ms_career', '0008_auto_20150709_1358'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='token',
            name='user',
        ),
        migrations.AddField(
            model_name='user',
            name='token',
            field=models.ForeignKey(default=1, to='786ms_career.Token'),
            preserve_default=False,
        ),
    ]

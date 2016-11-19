# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('786ms_career', '0010_auto_20150709_1648'),
    ]

    operations = [
        migrations.AddField(
            model_name='token',
            name='dob',
            field=models.DateField(default=datetime.datetime(2015, 7, 9, 14, 45, 1, 760850, tzinfo=utc), verbose_name=b'Date Of Birth'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='token',
            name='name',
            field=models.CharField(default='a', max_length=50),
            preserve_default=False,
        ),
    ]

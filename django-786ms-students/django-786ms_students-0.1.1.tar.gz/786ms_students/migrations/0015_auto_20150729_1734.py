# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('786ms_students', '0014_auto_20150729_1154'),
    ]

    operations = [
        migrations.AddField(
            model_name='studenttoken',
            name='by',
            field=models.ForeignKey(default=1, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='studenttoken',
            name='token',
            field=models.CharField(default=b'DB693FDD', unique=True, max_length=8, editable=False),
        ),
    ]

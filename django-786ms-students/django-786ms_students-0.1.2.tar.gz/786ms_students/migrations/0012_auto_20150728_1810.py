# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('786ms_students', '0011_auto_20150726_1845'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='left_thumb_impression',
            field=models.ImageField(upload_to=b'thumb_impressions'),
        ),
        migrations.AlterField(
            model_name='student',
            name='photo',
            field=models.ImageField(upload_to=b'photos'),
        ),
        migrations.AlterField(
            model_name='student',
            name='signature',
            field=models.ImageField(upload_to=b'signatures'),
        ),
        migrations.AlterField(
            model_name='studenttoken',
            name='token',
            field=models.CharField(default=b'427be5dd', unique=True, max_length=8, editable=False),
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('786ms_students', '0007_auto_20150726_1601'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='token',
            field=models.OneToOneField(related_name='student', primary_key=True, serialize=False, to='786ms_students.StudentToken'),
        ),
        migrations.AlterField(
            model_name='studenttoken',
            name='token',
            field=models.CharField(default=b'632fdcf0', unique=True, max_length=8, editable=False),
        ),
    ]

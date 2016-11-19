# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('786ms_students', '0009_auto_20150726_1756'),
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.AlterField(
            model_name='studenttoken',
            name='token',
            field=models.CharField(default=b'092c0f83', unique=True, max_length=8, editable=False),
        ),
        migrations.AddField(
            model_name='student',
            name='interested_in',
            field=models.ManyToManyField(to='786ms_students.Course'),
        ),
    ]

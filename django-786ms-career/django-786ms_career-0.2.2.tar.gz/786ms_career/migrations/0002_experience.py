# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('786ms_career', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Experience',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('exp_title', models.CharField(max_length=100)),
                ('duration', models.IntegerField()),
                ('summary', models.CharField(max_length=200)),
            ],
        ),
    ]

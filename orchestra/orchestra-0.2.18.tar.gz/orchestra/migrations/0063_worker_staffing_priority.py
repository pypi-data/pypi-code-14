# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-05-19 03:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orchestra', '0062_auto_20160515_1545'),
    ]

    operations = [
        migrations.AddField(
            model_name='worker',
            name='staffing_priority',
            field=models.IntegerField(default=0),
        ),
    ]

# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-02-11 09:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('simple_forums', '0004_auto_20160201_1656'),
    ]

    operations = [
        migrations.AddField(
            model_name='thread',
            name='slug',
            field=models.SlugField(default='default'),
            preserve_default=False,
        ),
    ]

# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-05-11 17:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0010_auto_20160511_0722'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='tracking_link',
            field=models.CharField(default='tracking link', max_length=250),
            preserve_default=False,
        ),
    ]

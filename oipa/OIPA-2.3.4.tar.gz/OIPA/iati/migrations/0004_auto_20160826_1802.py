# -*- coding: utf-8 -*-
# Generated by Django 1.9.9 on 2016-08-26 09:02
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('iati', '0003_auto_20160823_1800'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='description',
            unique_together=set([('activity', 'type', 'language')]),
        ),
    ]

# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-09-04 06:23
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('surveys', '0009_add_start_end_date'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='surveyfieldordering',
            options={'ordering': ['sort_order']},
        ),
        migrations.AlterModelOptions(
            name='surveyfieldsetordering',
            options={'ordering': ['sort_order']},
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='country',
            options={'ordering': ('sort_id',)},
        ),
        migrations.AlterModelOptions(
            name='environmentaltheme',
            options={'ordering': ('sort_id',)},
        ),
        migrations.AlterModelOptions(
            name='geographicalscope',
            options={'ordering': ('sort_id',)},
        ),
        migrations.AddField(
            model_name='country',
            name='sort_id',
            field=models.IntegerField(default=0, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='environmentaltheme',
            name='sort_id',
            field=models.IntegerField(default=0, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='geographicalscope',
            name='sort_id',
            field=models.IntegerField(default=0, null=True, blank=True),
            preserve_default=True,
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bibblio', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='metadata',
            options={
                'ordering': ('type', 'text'),
                'verbose_name': 'Metadata',
                'verbose_name_plural': 'Metadata'},
        ),
        migrations.RemoveField(
            model_name='bibblioidmap',
            name='catalog_id',
        ),
    ]

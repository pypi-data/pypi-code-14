# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sites', '0001_initial'),
        ('interviews', '0002_auto_20150707_1810'),
    ]

    operations = [
        migrations.AddField(
            model_name='quote',
            name='site',
            field=models.ForeignKey(default=2, to='sites.Site'),
        ),
    ]

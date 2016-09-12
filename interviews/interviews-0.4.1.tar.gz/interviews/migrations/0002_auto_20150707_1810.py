# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('interviews', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quote',
            name='related_to',
            field=models.ForeignKey(blank=True, to='interviews.Answer', null=True),
        ),
    ]

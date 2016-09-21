# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0013_content_hide_from_rss'),
    ]

    operations = [
        migrations.AlterField(
            model_name='content',
            name='template_choice',
            field=models.IntegerField(default=0, choices=[(0, None)]),
        ),
    ]

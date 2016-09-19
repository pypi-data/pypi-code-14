# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leonardo_module_links', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='link',
            name='category',
            field=models.ForeignKey(verbose_name='List', blank=True, to='leonardo_module_links.LinkCategory', null=True),
        ),
    ]

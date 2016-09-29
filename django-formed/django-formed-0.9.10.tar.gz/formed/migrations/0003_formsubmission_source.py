# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('formed', '0002_add_field_finish_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='formsubmission',
            name='source',
            field=models.CharField(help_text='This should give you more information on which form this form submission came from.', max_length=255, null=True, verbose_name='source', blank=True),
        ),
    ]

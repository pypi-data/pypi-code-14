# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('formed', '0005_formdefinition_confirmation_email_show_summary'),
    ]

    operations = [
        migrations.AddField(
            model_name='formsubmission',
            name='source_url',
            field=models.CharField(help_text='The URL of the page from which the form was submitted if available.', max_length=255, null=True, verbose_name='source page url', blank=True),
        ),
    ]

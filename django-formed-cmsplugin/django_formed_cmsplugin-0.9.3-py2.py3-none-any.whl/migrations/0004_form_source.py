# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cmsplugin_formed_form', '0003_form_finish_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='form',
            name='source',
            field=models.CharField(help_text="This should give more information about the page and location from which this form is submitted. Can be anything from a number or 'Bottom form on product page X'.", max_length=255, null=True, verbose_name='source', blank=True),
        ),
    ]

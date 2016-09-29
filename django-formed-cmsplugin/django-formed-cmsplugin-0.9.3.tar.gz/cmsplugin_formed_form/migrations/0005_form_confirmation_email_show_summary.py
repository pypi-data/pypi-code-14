# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cmsplugin_formed_form', '0004_form_source'),
    ]

    operations = [
        migrations.AddField(
            model_name='form',
            name='confirmation_email_show_summary',
            field=models.SmallIntegerField(default=-1, help_text='Uncheck to hide the submitted fields on the confirmation E-mail.', null=True, verbose_name='show field summary in confirmation E-mail', choices=[(-1, 'Inherit from form definition'), (1, 'Yes'), (0, 'No')]),
        ),
    ]

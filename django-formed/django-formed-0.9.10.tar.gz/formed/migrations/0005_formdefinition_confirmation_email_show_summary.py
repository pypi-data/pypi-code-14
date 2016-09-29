# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('formed', '0004_unique_together_formsubmission_notification'),
    ]

    operations = [
        migrations.AddField(
            model_name='formdefinition',
            name='confirmation_email_show_summary',
            field=models.BooleanField(default=True, help_text='Uncheck to hide the submitted fields on the confirmation E-mail.', verbose_name='show field summary in confirmation E-mail'),
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('formed', '0003_formsubmission_source'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='formsubmissionnotification',
            unique_together=set([('form_definition', 'email')]),
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import provider.utils


class Migration(migrations.Migration):

    dependencies = [
        ('oauth2', '0003_client_logout_uri'),
    ]

    operations = [
        migrations.AlterField(
            model_name='accesstoken',
            name='expires',
            field=models.DateTimeField(db_index=True),
        ),
        migrations.AlterField(
            model_name='grant',
            name='expires',
            field=models.DateTimeField(default=provider.utils.get_code_expiry, db_index=True),
        ),
        migrations.AlterIndexTogether(
            name='grant',
            index_together=set([('client', 'code', 'expires')]),
        ),
    ]

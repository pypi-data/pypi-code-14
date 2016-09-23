# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.utils.timezone import utc
from django.conf import settings
import django.db.models.deletion
import datetime


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('liveblog', '0004_auto_20160908_1512'),
    ]

    operations = [
        migrations.AddField(
            model_name='liveblogentry',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2016, 9, 19, 19, 36, 35, 21936, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='liveblogentry',
            name='created_by',
            field=models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='liveblogentry',
            name='updated',
            field=models.DateTimeField(default=datetime.datetime(2016, 9, 19, 19, 36, 47, 140826, tzinfo=utc), auto_now=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='liveblogentry',
            name='updated_by',
            field=models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, null=True, blank=True),
        ),
    ]

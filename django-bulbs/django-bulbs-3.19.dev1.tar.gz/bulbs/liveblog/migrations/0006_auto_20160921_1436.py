# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('liveblog', '0005_auto_20160919_1436'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='liveblogentry',
            options={'ordering': ['-published']},
        ),
        migrations.AlterField(
            model_name='liveblogresponse',
            name='author',
            field=models.ForeignKey(blank=True, to='blogger.Personality', null=True),
        ),
    ]

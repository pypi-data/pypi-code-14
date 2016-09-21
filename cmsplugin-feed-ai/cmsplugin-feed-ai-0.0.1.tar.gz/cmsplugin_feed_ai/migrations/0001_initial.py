# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0016_auto_20160608_1535'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProfileFeedPluginConf',
            fields=[
                ('cmsplugin_ptr', models.OneToOneField(serialize=False, to='cms.CMSPlugin', auto_created=True, related_name='cmsplugin_feed_ai_profilefeedpluginconf', parent_link=True, primary_key=True)),
                ('items_per_service', models.PositiveSmallIntegerField(verbose_name='number of items per service', default=5)),
            ],
            options={
                'abstract': False,
            },
            bases=('cms.cmsplugin',),
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('super_features', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='basesuperfeature',
            name='default_child_type',
            field=models.CharField(blank=True, max_length=255, null=True, choices=[(b'GUIDE_TO_HOMEPAGE', b'Guide To Homepage'), (b'GUIDE_TO_ENTRY', b'Guide To Entry'), (b'TO_WATCH_HOMEPAGE', b'To Watch Homepage'), (b'TO_WATCH_ENTRY', b'To Watch Entry'), (b'STATE_BY_STATE_LANDING', b'State by State Landing'), (b'STATE_BY_STATE_DETAIL', b'State by State Entry')]),
        ),
        migrations.AlterField(
            model_name='basesuperfeature',
            name='superfeature_type',
            field=models.CharField(max_length=255, choices=[(b'GUIDE_TO_HOMEPAGE', b'Guide To Homepage'), (b'GUIDE_TO_ENTRY', b'Guide To Entry'), (b'TO_WATCH_HOMEPAGE', b'To Watch Homepage'), (b'TO_WATCH_ENTRY', b'To Watch Entry'), (b'STATE_BY_STATE_LANDING', b'State by State Landing'), (b'STATE_BY_STATE_DETAIL', b'State by State Entry')]),
        ),
    ]

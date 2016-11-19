# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('786ms_career', '0011_auto_20150709_2015'),
    ]

    operations = [
        migrations.CreateModel(
            name='CCCUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('applied_before', models.BooleanField(default=False)),
                ('name', models.CharField(max_length=100)),
                ('care_of', models.CharField(max_length=100, choices=[(1, b'Parents'), (2, b'Gardians')])),
                ('father_name', models.CharField(max_length=100)),
                ('mother_name', models.CharField(max_length=100)),
                ('gender', models.CharField(max_length=100, choices=[(1, b'Male'), (2, b'Female'), (3, b'others')])),
                ('date_of_birth', models.DateField()),
                ('category', models.CharField(max_length=100, choices=[(1, b'General'), (2, b'SC'), (3, b'ST'), (4, b'Other Backward Classes')])),
                ('occupation', models.CharField(max_length=100, choices=[(1, b'Governament'), (2, b'Government undertaking'), (3, b'self employed'), (4, b'others')])),
            ],
        ),
    ]

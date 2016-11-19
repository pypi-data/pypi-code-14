# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0012_auto_20150728_1810'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='highest_educational_qualification',
            field=models.CharField(max_length=100, choices=[(b'Others', b'Others'), (b'Graduation or higher', b'Graduation or higher'), (b'Polytechnic Diploma', b'Polytechnic Diploma'), (b'Below 10th', b'Below 10th'), (b'10th Pass', b'10th Pass'), (b'12th Pass', b'12th Pass'), (b'10th + ITI', b'10th + ITI')]),
        ),
        migrations.AlterField(
            model_name='student',
            name='occupation',
            field=models.CharField(max_length=100, choices=[(b'Government', b'Government'), (b'Government undertaking', b'Government undertaking'), (b'self employed', b'self employed'), (b'others', b'others')]),
        ),
        migrations.AlterField(
            model_name='studenttoken',
            name='token',
            field=models.CharField(default=b'DDDB391E', unique=True, max_length=8, editable=False),
        ),
    ]

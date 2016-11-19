# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0005_auto_20150725_1210'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='student',
            name='applied_before',
        ),
        migrations.RemoveField(
            model_name='student',
            name='id',
        ),
        migrations.AddField(
            model_name='student',
            name='token',
            field=models.OneToOneField(primary_key=True, default=1, serialize=False, to='students.StudentToken'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='student',
            name='care_of',
            field=models.CharField(default=(b'Parents', b'Parents'), max_length=100, choices=[(b'Parents', b'Parents'), (b'Gardians', b'Gardians')]),
        ),
        migrations.AlterField(
            model_name='student',
            name='category',
            field=models.CharField(default=(b'General', b'General'), max_length=100, choices=[(b'General', b'General'), (b'SC', b'SC'), (b'ST', b'ST'), (b'Other Backward Classes', b'Other Backward Classes')]),
        ),
        migrations.AlterField(
            model_name='student',
            name='gender',
            field=models.CharField(default=(b'Male', b'Male'), max_length=100, choices=[(b'Male', b'Male'), (b'Female', b'Female'), (b'others', b'others')]),
        ),
        migrations.AlterField(
            model_name='student',
            name='left_thumb_impression',
            field=models.ImageField(upload_to=b'/home/zeeshan/Desktop/Websites/ms786-os/new/wsgi/openshift/images/thumb_impressions'),
        ),
        migrations.AlterField(
            model_name='student',
            name='photo',
            field=models.ImageField(upload_to=b'/home/zeeshan/Desktop/Websites/ms786-os/new/wsgi/openshift/images/photos'),
        ),
        migrations.AlterField(
            model_name='student',
            name='signature',
            field=models.ImageField(upload_to=b'/home/zeeshan/Desktop/Websites/ms786-os/new/wsgi/openshift/images/signatures'),
        ),
        migrations.AlterField(
            model_name='studenttoken',
            name='token',
            field=models.CharField(default=b'f2e1f6e0', unique=True, max_length=8, editable=False),
        ),
    ]

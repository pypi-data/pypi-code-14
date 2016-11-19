# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CCCUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('applied_before', models.BooleanField(default=False)),
                ('name', models.CharField(max_length=100)),
                ('care_of', models.CharField(max_length=100, choices=[(b'Parents', b'Parents'), (b'Gardians', b'Gardians')])),
                ('father_name', models.CharField(max_length=100)),
                ('mother_name', models.CharField(max_length=100)),
                ('gender', models.CharField(max_length=100, choices=[(b'Male', b'Male'), (b'Female', b'Female'), (b'others', b'others')])),
                ('date_of_birth', models.DateField()),
                ('category', models.CharField(max_length=100, choices=[(b'General', b'General'), (b'SC', b'SC'), (b'ST', b'ST'), (b'Other Backward Classes', b'Other Backward Classes')])),
                ('occupation', models.CharField(max_length=100, choices=[(b'Governament', b'Governament'), (b'Government undertaking', b'Government undertaking'), (b'self employed', b'self employed'), (b'others', b'others')])),
                ('mobile', models.CharField(max_length=10)),
                ('email', models.EmailField(max_length=254)),
                ('address', models.CharField(max_length=500)),
                ('city', models.CharField(max_length=100)),
                ('state', models.CharField(max_length=100)),
                ('distict', models.CharField(max_length=100)),
                ('pin_code', models.IntegerField()),
                ('highest_educational_qualification', models.CharField(max_length=100, choices=[(b'Others', b'Others'), (b'Graduation or heigher', b'Graduation or heigher'), (b'Polytechnic Diploma', b'Polytechnic Diploma'), (b'Below 10th', b'Below 10th'), (b'10th Pass', b'10th Pass'), (b'12th Pass', b'12th Pass'), (b'10th + ITI', b'10th + ITI')])),
                ('year_of_passing', models.IntegerField()),
                ('adhar_card_number', models.CharField(max_length=100)),
                ('photo', models.ImageField(upload_to=b'/images/786ms/cccusers/photos')),
                ('signature', models.ImageField(upload_to=b'/images/786ms/cccusers/signatures')),
                ('left_thumb_impression', models.ImageField(upload_to=b'/images/786ms/cccusers/thumb_impressions')),
            ],
        ),
        migrations.CreateModel(
            name='StudentToken',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('date_of_birth', models.DateField()),
                ('token', models.CharField(default=b'c9b5a87d', unique=True, max_length=8, editable=False)),
            ],
        ),
    ]

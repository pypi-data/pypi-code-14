# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Qualification',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('duration', models.IntegerField()),
                ('board', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Token',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('token', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('dob', models.DateTimeField(verbose_name=b'Date Of Birth')),
            ],
        ),
        migrations.AddField(
            model_name='token',
            name='user',
            field=models.ForeignKey(to='786ms_career.User'),
        ),
        migrations.AddField(
            model_name='qualification',
            name='user',
            field=models.ForeignKey(to='786ms_career.User'),
        ),
    ]

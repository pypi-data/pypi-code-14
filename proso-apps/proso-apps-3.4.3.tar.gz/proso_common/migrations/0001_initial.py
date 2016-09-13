# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-08-01 07:59
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Config',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('app_name', models.CharField(blank=True, max_length=100, null=True)),
                ('key', models.CharField(blank=True, max_length=100, null=True)),
                ('content', models.TextField()),
                ('content_hash', models.CharField(db_index=True, max_length=40)),
            ],
        ),
        migrations.CreateModel(
            name='CustomConfig',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('condition_key', models.CharField(blank=True, default=None, max_length=255, null=True)),
                ('condition_value', models.TextField(blank=True, default=None, null=True)),
                ('config', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='proso_common.Config')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]

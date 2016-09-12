# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-08-23 22:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('djmessenger', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Callback',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='FBUserProfile',
            fields=[
                ('psid', models.CharField(max_length=512, primary_key=True, serialize=False)),
                ('first_name', models.CharField(blank=True, max_length=512, null=True, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=512, null=True, verbose_name='last name')),
                ('profile_pic', models.TextField(blank=True, null=True)),
                ('locale', models.CharField(blank=True, max_length=128, null=True)),
                ('timezone', models.SmallIntegerField()),
                ('gender', models.CharField(blank=True, max_length=20, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('date_joined', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='GetStartedButton',
            fields=[
                ('payload', models.CharField(help_text='The payload string will be sent back to you via Postback,so once you added a Get Started Button here, you also need to define how to handle the payload', max_length=160, primary_key=True, serialize=False, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='PersistentMenu',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('postback', 'postback'), ('web_url', 'web_url')], default='web_url', help_text='postback means when clicking on the menu, it will send the payload back to the server; while web_url simply opensthe url', max_length=10)),
                ('title', models.CharField(help_text='Button title', max_length=30)),
                ('url', models.URLField(help_text='For web_url buttons, this URL is opened in a mobile browser when the button is tapped')),
                ('payload', models.CharField(help_text='For postback buttons, this data will be sent back to you via webhook', max_length=1000)),
            ],
        ),
    ]

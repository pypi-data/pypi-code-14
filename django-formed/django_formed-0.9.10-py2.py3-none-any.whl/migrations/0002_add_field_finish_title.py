# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('formed', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='formsubmissionnotification',
            options={'verbose_name': 'form submission notification recipient', 'verbose_name_plural': 'form submission notification recipients'},
        ),
        migrations.AddField(
            model_name='formdefinition',
            name='finish_title',
            field=models.CharField(help_text='Title displayed on the page if the form is submitted. If left empty the default text will be displayed. Possible placeholders are: {first_name}, {last_name_prefix}, {last_name} or {full_name} (the users name, when available in the form), {form_name}, {submit_language} (user language) and {submit_site} (the site from which the form was submitted.).', max_length=255, null=True, verbose_name='finish title', blank=True),
        ),
    ]

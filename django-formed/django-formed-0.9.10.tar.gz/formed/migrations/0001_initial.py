# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import jsonfield.fields
import django.utils.translation


class Migration(migrations.Migration):

    dependencies = [
        ('sites', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='FormDefinition',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255, verbose_name='name')),
                ('slug', models.SlugField(max_length=255, verbose_name='slug')),
                ('definition', jsonfield.fields.JSONField(verbose_name='definition')),
                ('enable_summary', models.BooleanField(default=True, help_text='Check to enable the summary page which displays an overview of all submitted data and gives the user the opportunity to double check their submission.', verbose_name='enable summary page')),
                ('send_confirmation_email', models.BooleanField(default=True, help_text='Check to enable sending of a confirmation E-mail to the person who submitted the form. This requires an E-mail field to be present in the form. By default the confirmation E-mail field is used. If there is none, the value of the first E-mail field will be used.', verbose_name='send confirmation E-mail')),
                ('confirmation_email_subject', models.CharField(help_text="The subject of the E-mail that is sent to the person who submitted the form. For example: 'Thank you for your message!'. Possible placeholders are: {first_name}, {last_name_prefix}, {last_name} or {full_name} (the users name, when available in the form), {form_name}, {submit_language} (user language) and {submit_site} (the site from which the form was submitted.).", max_length=254, null=True, verbose_name='confirmation E-mail subject', blank=True)),
                ('confirmation_email_text', models.TextField(help_text='The text displayed at the top of the E-mail that is sent to the person who submitted the form. Possible placeholders are: {first_name}, {last_name_prefix}, {last_name} or {full_name} (the users name, when available in the form), {form_name}, {submit_language} (user language) and {submit_site} (the site from which the form was submitted.).', null=True, verbose_name='confirmation E-mail text', blank=True)),
                ('notification_email_subject', models.CharField(default="Submission of the form '{form_name}'", help_text='The subject of the E-mail that is sent to the users that are notified of form submissions. Possible placeholders are: {first_name}, {last_name_prefix}, {last_name} or {full_name} (the users name, when available in the form), {form_name}, {submit_language} (user language) and {submit_site} (the site from which the form was submitted.).', max_length=254, verbose_name='notification E-mail subject')),
                ('finish_text', models.TextField(help_text='Text displayed on the page if the form is submitted. If left empty the default text will be displayed. Possible placeholders are: {first_name}, {last_name_prefix}, {last_name} or {full_name} (the users name, when available in the form), {form_name}, {submit_language} (user language) and {submit_site} (the site from which the form was submitted.).', null=True, verbose_name='finish text', blank=True)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='modified')),
                ('sites', models.ManyToManyField(help_text='The sites on which this form is available.', to='sites.Site', verbose_name='available on', blank=True)),
            ],
            options={
                'verbose_name': 'form',
                'verbose_name_plural': 'forms',
            },
        ),
        migrations.CreateModel(
            name='FormSubmission',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('submission', jsonfield.fields.JSONField(verbose_name='submission')),
                ('language', models.CharField(default=django.utils.translation.get_language, help_text='The language in which the submitter was using the website when the form was submitted.', max_length=10, verbose_name='language')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='modified')),
                ('form_definition', models.ForeignKey(verbose_name='form', to='formed.FormDefinition')),
                ('site', models.ForeignKey(blank=True, to='sites.Site', help_text='The site on which the form was submitted.', null=True, verbose_name='submitted on site')),
            ],
            options={
                'verbose_name': 'form submission',
                'verbose_name_plural': 'form submissions',
            },
        ),
        migrations.CreateModel(
            name='FormSubmissionNotification',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('email', models.EmailField(max_length=254, verbose_name='E-mail')),
                ('name', models.CharField(max_length=255, null=True, verbose_name='name', blank=True)),
                ('copy', models.CharField(blank=True, max_length=3, null=True, verbose_name='send as copy', choices=[(b'cc', 'CC'), (b'bcc', 'BCC')])),
                ('form_definition', models.ForeignKey(verbose_name='form', to='formed.FormDefinition')),
            ],
        ),
    ]

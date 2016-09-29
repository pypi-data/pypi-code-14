# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cmsplugin_formed_form', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='FormPluginSubmissionNotification',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('email', models.EmailField(max_length=254, verbose_name='E-mail')),
                ('name', models.CharField(max_length=255, null=True, verbose_name='name', blank=True)),
                ('copy', models.CharField(blank=True, max_length=3, null=True, verbose_name='send as copy', choices=[('cc', 'CC'), ('bcc', 'BCC')])),
            ],
            options={
                'verbose_name': '(Additional) form submission notification recipient',
                'verbose_name_plural': '(Additional) form submission notification recipients',
            },
        ),
        migrations.AddField(
            model_name='form',
            name='confirmation_email_subject',
            field=models.CharField(help_text="The subject of the E-mail that is sent to the person who submitted the form. For example: 'Thank you for your message!' Possible placeholders are: {first_name}, {last_name_prefix}, {last_name} or {full_name} (the users name, when available in the form), {form_name}, {submit_language} (user language) and {submit_site} (the site from which the form was submitted.).", max_length=254, null=True, verbose_name='confirmation E-mail subject', blank=True),
        ),
        migrations.AddField(
            model_name='form',
            name='confirmation_email_text',
            field=models.TextField(help_text='The text displayed at the top of the E-mail that is sent to the person who submitted the form. Possible placeholders are: {first_name}, {last_name_prefix}, {last_name} or {full_name} (the users name, when available in the form), {form_name}, {submit_language} (user language) and {submit_site} (the site from which the form was submitted.).', null=True, verbose_name='confirmation E-mail text', blank=True),
        ),
        migrations.AddField(
            model_name='form',
            name='enable_summary',
            field=models.SmallIntegerField(default=-1, help_text='Check to enable the summary page which displays an overview of all submitted data and gives the user the opportunity to double check their submission.', null=True, verbose_name='enable summary page', choices=[(-1, 'Inherit from form definition'), (1, 'Yes'), (0, 'No')]),
        ),
        migrations.AddField(
            model_name='form',
            name='finish_text',
            field=models.TextField(help_text='Text displayed on the page if the form is submitted. If left empty the default text will be displayed.Possible placeholders are: {first_name}, {last_name_prefix}, {last_name} or {full_name} (the users name, when available in the form), {form_name}, {submit_language} (user language) and {submit_site} (the site from which the form was submitted.).', null=True, verbose_name='finish text', blank=True),
        ),
        migrations.AddField(
            model_name='form',
            name='inherit_submission_notifications',
            field=models.BooleanField(default=True, help_text="Uncheck if you don't want to inherit the notification recipients from the form. Only the recipients added to this plugin are used.", verbose_name='inherit notification recipients?'),
        ),
        migrations.AddField(
            model_name='form',
            name='notification_email_subject',
            field=models.CharField(help_text='The subject of the E-mail that is sent to the users that are notified of form submissions. Possible placeholders are {name} (form name), {language} (user language) and {site} (the site).Possible placeholders are: {first_name}, {last_name_prefix}, {last_name} or {full_name} (the users name, when available in the form), {form_name}, {submit_language} (user language) and {submit_site} (the site from which the form was submitted.).', max_length=254, null=True, verbose_name='notification E-mail subject', blank=True),
        ),
        migrations.AddField(
            model_name='form',
            name='send_confirmation_email',
            field=models.SmallIntegerField(default=-1, help_text='Check to enable sending of a confirmation E-mail to the person who submitted the form. This requires an E-mail field to be present in the form. By default the value of the first E-mail field will be used.', null=True, verbose_name='send confirmation E-mail', choices=[(-1, 'Inherit from form definition'), (1, 'Yes'), (0, 'No')]),
        ),
        migrations.AddField(
            model_name='formpluginsubmissionnotification',
            name='form_definition',
            field=models.ForeignKey(verbose_name='form', to='cmsplugin_formed_form.Form'),
        ),
    ]

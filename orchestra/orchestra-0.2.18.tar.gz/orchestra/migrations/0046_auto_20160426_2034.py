# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-26 20:34
from __future__ import unicode_literals

from enum import Enum

from django.db import migrations

# Copy pasted from models since migrations does not have access
class CommunicationMethods(object):
    SLACK = 'slack'
    EMAIL = 'email'


COMMUNICATION_METHODS = (
    (CommunicationMethods.SLACK, 'Slack'),
    (CommunicationMethods.EMAIL, 'Email'),
)

class CommunicationType(Enum):
    TASK_STATUS_CHANGE = 0

def add_communcation_type_to_workers(apps, schema_editor):
    CommunicationPreference = apps.get_model(
        'orchestra', 'CommunicationPreference')
    Worker = apps.get_model('orchestra', 'Worker')

    default_methods = 2**len(COMMUNICATION_METHODS) - 1
    for worker in Worker.objects.all():
        CommunicationPreference.objects.get_or_create(
            worker=worker,
            methods=default_methods,
            communication_type=CommunicationType.TASK_STATUS_CHANGE.value)


class Migration(migrations.Migration):

    dependencies = [
        ('orchestra', '0045_auto_20160426_2034'),
    ]

    operations = [
        migrations.RunPython(add_communcation_type_to_workers)  # manually-reviewed
    ]

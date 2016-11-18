# -*- coding: utf-8 -*-
"""
After configuring :data:`djmessenger.settings.DJM_THREAD_SETTINGS_URL` and
:data:`djmessenger.settings.DJM_THREAD_GREETINGS_TEXT`, call this
management command to actually configure Greetings
"""
import requests
import logging


from django.core.management.base import BaseCommand

from djmessenger.settings import DJM_THREAD_SETTINGS_URL, DJM_THREAD_GREETINGS_TEXT


logger = logging.getLogger(__name__)


class Command(BaseCommand):
    def handle(self, *args, **options):
        logger.debug('Ready to configure Greetings')
        data = {
            "setting_type": "greeting",
            "greeting": {
                "text": str(DJM_THREAD_GREETINGS_TEXT)
            }
        }
        logger.debug('Prepared payload for configuring Greetings as %s'
                     % data)
        status = requests.post(DJM_THREAD_SETTINGS_URL,
                               headers={"Content-Type": "application/json"},
                               json=data)
        print(status.content)
        logger.debug('Configuring greetings got response code %s, content %s'
                     % (status.status_code, status.content))


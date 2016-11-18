# -*- coding: utf-8 -*-
"""
After configuring :data:`djmessenger.settings.DJM_THREAD_SETTINGS_URL` and
:data:`djmessenger.settings.DJM_THREAD_ENABLE_GET_STARTED_BUTTON`, call this
management command to actually configure get started button
"""
import requests
import logging

from django.core.management.base import BaseCommand

from djmessenger.settings import DJM_THREAD_SETTINGS_URL, DJM_THREAD_ENABLE_GET_STARTED_BUTTON
from djmessenger.payload import GetStartedPayload


logger = logging.getLogger(__name__)


class Command(BaseCommand):
    def handle(self, *args, **options):
        logger.debug('Ready to configure Get Started Button')
        if not DJM_THREAD_ENABLE_GET_STARTED_BUTTON:
            logger.debug('DJM_THREAD_ENABLE_GET_STARTED_BUTTON was set to '
                         'False, not configuring')
            return
        data = {
            "setting_type": "call_to_actions",
            "thread_state": "new_thread",
            "call_to_actions": [
                {
                    "payload": GetStartedPayload().serialize()
                }
            ]
        }
        logger.debug('Prepared payload for configuring Get Started Button as %s'
                     % data)
        status = requests.post(DJM_THREAD_SETTINGS_URL,
                               headers={"Content-Type": "application/json"},
                               json=data)
        logger.debug('Configuring Get Started Button got response code %s, '
                     'content %s' % (status.status_code, status.content))

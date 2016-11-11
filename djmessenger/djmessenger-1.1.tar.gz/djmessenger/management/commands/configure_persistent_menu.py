# -*- coding: utf-8 -*-
"""
After configuring :data:`djmessenger.settings.DJM_THREAD_PERSISTENT_MENUS`,
call this management command to actually configure the persistent menu
"""
import requests
import gettext
import logging

from django.core.management.base import BaseCommand

from djmessenger.settings import DJM_THREAD_SETTINGS_URL, DJM_THREAD_PERSISTENT_MENUS
from djmessenger.payload import *


logger = logging.getLogger(__name__)


class Command(BaseCommand):
    def handle(self, *args, **options):
        logger.debug('Ready to configure Persistent Menu')
        if not DJM_THREAD_PERSISTENT_MENUS:
            return
        actions = []
        # let index starts from 1
        for index in range(1, len(DJM_THREAD_PERSISTENT_MENUS) + 1):
            item = DJM_THREAD_PERSISTENT_MENUS[index-1]
            if index > 5:
                logger.debug('Facebook only permits 5 Persistent Menu items, '
                             'this item is the %d item, skipping' % index)
                break
            if 'title' not in item:
                logger.debug('There is no title in item, skipping')
                continue
            if 'url' in item:
                ttype = 'web_url'
                actions.append({
                    "type": ttype,
                    "title": item['title'],
                    "url": item['url']
                })
            else:
                ttype = 'postback'
                if index == 1:
                    payload = PersistentMenuOnePayload().serialize()
                elif index == 2:
                    payload = PersistentMenuTwoPayload().serialize()
                elif index == 3:
                    payload = PersistentMenuThreePayload().serialize()
                elif index == 4:
                    payload = PersistentMenuFourPayload().serialize()
                elif index == 5:
                    payload = PersistentMenuFivePayload().serialize()
                actions.append({
                    "type": ttype,
                    "title": item['title'],
                    "payload": payload
                })

        data = {
            "setting_type": "call_to_actions",
            "thread_state": "existing_thread",
            "call_to_actions": actions
        }
        logger.debug('Prepared payload for configuring Persistent Menu as %s'
                     % data)
        status = requests.post(DJM_THREAD_SETTINGS_URL,
                               headers={"Content-Type": "application/json"},
                               json=data)
        print(status.content)
        logger.debug('Configuring Persistent Menu got response code %s, '
                     'content %s' % (status.status_code, status.content))

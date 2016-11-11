# -*- coding: utf-8 -*-
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
import os
from djmessenger.utils.default_routing_policy import DJM_DEFAULT_ROUTING_POLICY

DJM_BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DJM_PAGE_ACCESS_TOKEN = getattr(settings, 'DJM_PAGE_ACCESS_TOKEN', '')
"""Facebook Page Access Token, get it from developers.facebook.com"""

DJM_ENDPOINT = getattr(settings, 'DJM_ENDPOINT', '')
"""The endpoint that Facebook will relay the callback message to
also being used to setup webhook"""

DJM_ENDPOINT_VERIFY_TOKEN = getattr(settings, 'DJM_ENDPOINT_VERIFY_TOKEN', 'djmessenger_verify_token')
"""Verify Token to be used when verifying endpoint in developer.facebook.com
"""

DJM_POST_MESSAGE_URL = getattr(settings, 'DJM_POST_MESSAGE_URL',
                               'https://graph.facebook.com/v2.6/me/messages?access_token=%s' % DJM_PAGE_ACCESS_TOKEN)

DJM_USER_DETAILS_URL = getattr(settings, 'DJM_USER_DETAILS_URL',
                               'https://graph.facebook.com/v2.6/%s')

DJM_THREAD_SETTINGS_URL = getattr(settings, 'DJM_THREAD_SETTINGS_URL',
                                  'https://graph.facebook.com/v2.6/me/thread_settings?access_token=%s' % DJM_PAGE_ACCESS_TOKEN)

DJM_SAVE_USER_PROFILE = getattr(settings, 'DJM_SAVE_USER_PROFILE', True)
"""Whether DJM should automatically fetch and save user profile for any user that
sends message to the page and observed by BOT, default to True"""


DJM_DEFAULT_SENDER_TEXT = getattr(settings, 'DJM_DEFAULT_SENDER_TEXT',
                                  'Thanks for your message')
"""A sender named djmessenger.sending.DefaultSender which is a SimpleTextSender
you can define your message here and directly use it in DJM_ROUTING_POLICY"""

DJM_BOT_PREFIX = getattr(settings, 'DJM_BOT_PREFIX', "BOT: ")
"""Prefix this string to all text messages sent to users"""

DJM_BUSINESS_ADDRESS = getattr(settings, 'DJM_BUSINESS_ADDRESS', '')
"""This address is where your business is located at"""

DJM_ROUTING_POLICY = getattr(settings, 'DJM_ROUTING_POLICY',
                             DJM_DEFAULT_ROUTING_POLICY)
"""
==================
DJM_ROUTING_POLICY
==================

DJM_ROUTING_POLICY defines the lifecycle of a message being received, handling
it and lastly send some response back. In the following format, each router
represents a type of message received, handlers represent which handlers should
be used to handle this type of message and lastly which senders should be used
to send the response back.

See :mod:`djmessenger.utils.default_routing_policy` for more details
"""

DJM_THREAD_GREETINGS_TEXT = getattr(settings, 'DJM_THREAD_GREETINGS_TEXT',
                                    "Welcome to the page!")
"""
https://developers.facebook.com/docs/messenger-platform/thread-settings/greeting-text

1. length must be <= 160
2. only first time visitor sees this greeting text
"""
"""
https://developers.facebook.com/docs/messenger-platform/thread-settings/persistent-menu

1. Only allow at most 5 menu items
2. Items without url will send a Postback Message to the server just like a Button
3. Items with url will simply open that url on a browser
4. title has 30 char limit
5. The order of items will be displayed to the user in the same order here
"""

DJM_THREAD_PERSISTENT_MENUS = getattr(settings, 'DJM_THREAD_PERSISTENT_MENUS',
                                      [
                                          {
                                              "title": "Help",
                                          },
                                          {
                                              "title": "Visit Website",
                                              "url": ""
                                          }
                                      ])
DJM_THREAD_ENABLE_GET_STARTED_BUTTON = getattr(
    settings, 'DJM_THREAD_ENABLE_GET_STARTED_BUTTON', False)
"""
https://developers.facebook.com/docs/messenger-platform/thread-settings/get-started-button
Whether to enable get started button feature
"""

# TODO: not implemented yet
DJM_THREAD_ENABLE_AUTO_CONFIG = getattr(
    settings, 'DJM_THREAD_ENABLE_AUTO_CONFIG', False)
"""
If set to True, djmessenger will send POST request to configure thread
automatically. If set to False, you need to configure it by using management
commands
"""

# prechecks
if not DJM_PAGE_ACCESS_TOKEN or not DJM_ENDPOINT:
    raise ImproperlyConfigured(
        'djmessenger requires at least DJM_PAGE_ACCESS_TOKEN and DJM_ENDPOINT'
        ' to be configured in your settings.py'
    )

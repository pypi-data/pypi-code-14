""" Copyright 2015 Will Boyce """
from __future__ import print_function, unicode_literals

import os
import random
try:
    import urlparse
except ImportError:
    import urllib.parse as urlparse

import requests

from telegrambot import util
from telegrambot.exceptions import TelegramBadRequestError
from telegrambot.plugins.base import BasePlugin


class BingSearch(BasePlugin):
    locale = 'en-GB'

    commands = {
        'get': 'get_image',
    }

    def get_image(self, args, msg, retries=4):
        self.send_chat_action('typing', to=msg.chat.id)
        query = ' '.join(args)
        result = self._get_random_result(query)
        if result is None:
            return msg.reply('No results found :(')
        self.send_chat_action('upload_photo', to=msg.chat.id)
        img_fn = util.download_tmp_file(self._get_result_url(result))
        try:
            self.send_photo(msg.chat.id, img_fn, result['name'], reply_to_message_id=msg.message_id)
        except TelegramBadRequestError:
            if retries > 0:
                self.get_image(args, msg, retries - 1)
        finally:
            os.unlink(img_fn)

    def _get_result_url(self, result):
        return urlparse.parse_qs(urlparse.urlparse(result['contentUrl']).query)['r'][0]

    def _get_random_result(self, *args, **kwargs):
        try:
            return random.choice(self._search(*args, **kwargs))
        except IndexError:
            pass

    def _search(self, query):
        if not self.bot.cfg.bing.key:
            return []
        url = 'https://api.cognitive.microsoft.com/bing/v5.0/images/search'
        params = {
            'q': query,
            'count': 100,
            'safeSearch': 'Off'
        }
        headers = {
            'Ocp-Apim-Subscription-Key': self.bot.cfg.bing.key,
        }
        data = requests.post(url, params=params, headers=headers).json()
        return data['value'] if 'value' in data else []

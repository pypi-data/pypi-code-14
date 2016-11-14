# vim: set fileencoding=utf8 :
from __future__ import print_function, unicode_literals

import os

import requests

from telegrambot import util
from telegrambot.plugins.base import BasePlugin


def trim_caption(str, maxlen=200, overflow_append=''):
    if len(str) < maxlen:
        return str
    cutoff = maxlen - 1
    if len(overflow_append) > 0:
        cutoff -= (len(overflow_append) + 1)
        overflow_append = ' {}'.format(overflow_append)
    return '{}…{}'.format(str[:cutoff], overflow_append)

class XKCD(BasePlugin):
    commands = {'xkcd': 'handle_cmd'}

    def handle_cmd(self, args, msg):
        path = ''
        if args:
            try:
                id = int(args[0])
                path = '/{}/'.format(id)
            except (IndexError, ValueError):
                pass
        url = 'http://xkcd.com/{}info.0.json'.format(path)
        data = requests.get(url).json()
        try:
            img_fn = util.download_tmp_file(data['img'])
            caption = trim_caption(data['alt'], overflow_append='http://xkcd.com/{}'.format(data['num']))
            self.send_photo(msg.chat.id, img_fn, caption=caption, reply_to_message_id=msg.message_id)
        finally:
            os.unlink(img_fn)
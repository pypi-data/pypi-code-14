""" Copyright 2015 Will Boyce """
from __future__ import print_function, unicode_literals

import json
import logging
import hashlib

from telegrambot.plugins.base import BasePlugin


class Logger(BasePlugin):
    def __init__(self, *args, **kwargs):
        super(Logger, self).__init__(*args, **kwargs)
        self.loggers = {}

    def handle_msg(self, msg):
        chat_id = hashlib.md5(str(msg.chat.id)).hexdigest()
        if chat_id not in self.loggers:
            logger = logging.getLogger('telegramlog.{}'.format(chat_id))
            logger.setLevel(logging.DEBUG)
            handler = logging.FileHandler('{}.log'.format(chat_id))
            handler.setFormatter(logging.Formatter('%(message)s'))
            logger.addHandler(handler)
            self.loggers[chat_id] = logger
        log_message = "{timestamp}:{chat_id}::{user} PRIVMSG {chat_id}:{msg_text}".format(**{
            'timestamp': msg.date.strftime("%Y-%m-%d-%H-%M-%S"),
            'chat_id': chat_id,
            'user': msg.froom.username or '{} {}'.format(msg.froom.first_name, msg.froom.last_name).strip().replace(' ', '_'),
            'msg_text': msg.text
        })
        self.loggers[chat_id].info(log_message)

    def handle_update(self, payload):
        self.logger.debug('handle_update(%s)', payload)

    # TODO: test/finish the pisg functions
    def pisg_normalline(self, chat_id, msg):
        payload = dict(hour=msg.date.hour,
                       nick=msg.froom.name,
                       saying=msg.text)
        self.pisg_log('normalline', payload)

    def pisg_actionline(self, msg):
        payload = dict(hour=msg.date.hour,
                       nick=msg.froom.name,
                       saying=msg.text)
        self.pisg_log('actionline', payload)

    def pisg_thirdline(self, msg):
        payload = dict(hour=msg.date.hour,
                       min=msg.date.min,
                       nick=msg.froom.name)
        if msg.left_chat_participant is not None:
            payload['nick'] = msg.left_chat_participant.name
            payload['kicker'] = msg.froom.name
        if msg.new_chat_participant:
            payload['newjoin'] = msg.left_chat_participant.name
        if msg.new_chat_title is not None:
            payload['newtopic'] = msg.new_chat_title
        self.pisg_log('thirdline', payload)

    def pisg_log(self, chat_id, pisg_type, payload):
        msg = '{} {}'.format(pisg_type, json.dumps(payload))
        self.loggers[chat_id].info(msg)

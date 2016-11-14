""" Copyright 2015 Will Boyce """
from __future__ import print_function, unicode_literals

from telegrambot.plugins.base import BasePlugin


class TechSupport(BasePlugin):
    def __init__(self, *args, **kwargs):
        super(TechSupport, self).__init__(*args, **kwargs)
        self.requests_map = {}
        if self.bot.cfg.techsupport and self.bot.cfg.techsupport.group_id:
            self.cfg = self.bot.cfg.techsupport
            self.cfg.group_id = int(self.cfg.group_id)
            self.commands = {
                'help': 'handle_help',
                'techsupport': 'handle_help',
                'broadcast': 'handle_broadcast',
            }

    def forward_request(self, msg, text=None):
        if text is None:
            text = msg.text
        return self.send_message('[Tech Support] {}\n\n{}'.format(msg.froom.name, text), self.cfg.group_id)

    def handle_help(self, args, msg):
        if msg.chat.id == self.cfg.group_id:
            return msg.reply(
                "Trying to use Tech Support from the Tech Support Group results in really confusing shit, don't do it.")
        if not args:
            return msg.reply("Leave a message and somebody will get back to you ASAP.")
        reply = self.forward_request(msg, ' '.join(args))
        self.requests_map[reply.message_id] = msg

    def handle_broadcast(self, args, msg):
        if msg.chat.id != self.cfg.group_id:
            return
        if not args:
            return msg.reply("I need a message to broadcast!")
        text = ' '.join(args)
        for room in self.bot.stats['rooms'].itervalues():
            print(room)
            if room.type != "private" and room.id != self.cfg.group_id:
                fwd = self.send_message(text, room.id)
                self.requests_map[fwd.message_id] = msg

    def handle_reply(self, msg):
        if msg.text:
            reply_to_id = msg.reply_to_message.message_id
            if reply_to_id not in self.requests_map:
                return

            if msg.chat.id == self.cfg.group_id:
                support_request = self.requests_map[msg.reply_to_message.message_id]
                reply = self.send_message(msg.text, support_request.chat.id,
                                          reply_to_message_id=support_request.message_id)
            else:
                reply = self.forward_request(msg)
            self.requests_map[reply.message_id] = msg

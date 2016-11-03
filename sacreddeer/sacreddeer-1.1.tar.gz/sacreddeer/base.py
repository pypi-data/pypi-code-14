#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import time

import slackclient

logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s',
                    level=logging.INFO)


class Bot(object):
    def __init__(self, name, token, visible_name=None):
        self.name = name
        self.visible_name = visible_name or name
        self.client = slackclient.SlackClient(token)
        self.bot_id = self._get_bot_id()

    def _get_bot_id(self):
        api_call = self.client.api_call("users.list")
        if api_call.get('ok'):
            # retrieve all users so we can find our bot
            users = api_call.get('members')
            for user in users:
                if 'name' in user and user.get('name') == self.name:
                    return user.get('id')
        else:
            raise LookupError("Could not find bot user with the name " +
                              self.name)

    def validate_command(self, cmd):
        """To be defined in child classes"""
        pass

    def prepare_response(self, cmd):
        """To be defined in child classes"""
        return "Hello!"

    def handle_command(self, cmd, chan):
        """
            Receives commands directed at the bot and determines if they
            are valid commands. If so, then acts on the commands. If not,
            returns back what it needs for clarification.
        """
        self.validate_command(cmd)
        response = self.prepare_response(cmd)
        self.client.api_call("chat.postMessage", channel=chan,
                             text=response, as_user=True)
        logging.info('Command: "%s", response: "%s"', cmd, response)

    def parse_slack_output(self, slack_rtm_output):
        """
            The Slack Real Time Messaging API is an events firehose.
            This parsing function returns None unless a message is
            directed at the Bot, based on its ID.
        """
        at_bot = "<@" + self.bot_id + ">"

        output_list = slack_rtm_output
        if output_list and len(output_list) > 0:
            for output in output_list:
                if output and 'text' in output and at_bot in output['text']:
                    # return text after the @ mention, whitespace removed
                    return output['text'].split(at_bot)[1].strip().lower(), \
                           output['channel']
        return None, None

    def run(self, read_socket_delay=1):
        if self.client.rtm_connect():
            logging.info("%s is connected and running!", self.visible_name)
            while True:
                command, channel = self.parse_slack_output(
                    self.client.rtm_read())
                if command and channel:
                    self.handle_command(command, channel)
                time.sleep(read_socket_delay)
        else:
            logging.error("Connection failed. Invalid Slack token or bot ID?")

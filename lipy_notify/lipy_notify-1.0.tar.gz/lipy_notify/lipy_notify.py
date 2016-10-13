# -*- coding: utf-8 -*-
import sys
import requests


class LipyNotify(object):

    def __init__(self):
        self.url = "https://notify-api.line.me/api/notify"
        self.headers = {
            "Content-Type": "application/x-www-form-urlencoded"
        }
        self.token = None

    def set_token(self, token):
        self.token = token
        self.headers["Authorization"] = "Bearer " + token

    def send(self, message):
        if self.token is None:
            sys.stderr.write("Message can't be sent. You must set your authorization token with set_token()")
        else:
            payload = {"message": message}
            requests.post(self.url, data=payload, headers=self.headers)

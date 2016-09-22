# -*- coding: utf-8 -*-
from __future__ import print_function
import json


class User(object):
    def __init__(self, username, password, remaining_request=100):
        self.username = username
        self.password = password
        self.remaining_request = remaining_request

    def __str__(self):
        return json.dumps({'username': self.username, 'password': self.password, 'remaining_request': self.remaining_request})

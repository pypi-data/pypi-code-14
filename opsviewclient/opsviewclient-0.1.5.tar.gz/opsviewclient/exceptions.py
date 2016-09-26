#!/usr/bin/env python
# coding: utf-8


class OpsviewClientException(Exception):

    def __init__(self, message, response=None):
        message = (message + response if response else message)
        super(OpsviewClientException, self).__init__(message)
        self.response = response

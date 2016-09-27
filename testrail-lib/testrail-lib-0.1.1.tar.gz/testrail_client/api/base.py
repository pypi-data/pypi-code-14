#!/usr/bin/env python                                                                                                                                                
# -*- coding: utf-8 -*-

import requests
from error import TesRailAPIError, TestRailAuthError


def check_execption(func):
    def _check(*arg, **kws):
        resp = func(*arg, **kws)
        if resp.status_code >= 400:
            if resp.status_code == 403:
                raise TestRailAuthError(403, 'No permission')
            elif resp.status_code == 401:
                raise TestRailAuthError(401, 'Not authorized')
            else:
                raise TesRailAPIError(resp)
        try:
            return resp.json()
        except Exception:
            return resp.content
    return _check


def format_request_filter(func):
    def _format(*args, **kwargs):
        params = kwargs.get('params', dict())
        for key in params:
            if isinstance(params[key], list):
                params[key] = ','.join(map(str, params[key]))
        return func(*args, **kwargs)
    return _format


class TestRailAPIBase(object):

    def __init__(self, url, user_name, password):
        self.url = url
        self.user_name = user_name
        self.password = password
        self.header = {
            'Content-Type': 'application/json'
        }

    def __repr__(self):
        return '<TestRailAPI Base>'

    @format_request_filter
    @check_execption
    def _get(self, url, **opts):
        return requests.get(self.url + url,
                            auth=(self.user_name, self.password),
                            headers=self.header,
                            **opts)

    @check_execption
    def _post(self, url, **opts):
        return requests.post(self.url + url,
                             auth=(self.user_name, self.password),
                             headers=self.header,
                             **opts)

# !/usr/bin/env python

# -*- coding:utf-8 -*-
# Shiny Python SDK
import collections
import hashlib
import json

import requests

from Shiny import config


class ShinyError(Exception):
    def __init__(self, message):
        self.message = message


class Shiny:
    def __init__(self, api_key, api_secret_key):
        self.API_KEY = api_key
        self.API_SECRET_KEY = api_secret_key

    def add(self, spider_name, level, data=None, hash=False):
        """添加数据项"""
        if data is None:
            data = {}

        url = config.API_HOST + '/Data/add'

        payload = {"api_key": self.API_KEY}

        event = {"level": level, "spiderName": spider_name}

        # 如果没有手动指定Hash，将会把data做一次md5生成hash
        try:
            if hash:
                event["hash"] = hash
            else:
                m = hashlib.md5()
                m.update(json.dumps(collections.OrderedDict(sorted(data.items()))).encode('utf-8'))
                event["hash"] = m.hexdigest()
        except Exception as e:
            raise ShinyError('Fail to generate hash')

        event["data"] = data

        sha1 = hashlib.sha1()
        sha1.update((config.API_KEY + config.API_SECRET_KEY + json.dumps(event)).encode('utf-8'))

        payload["sign"] = sha1.hexdigest()
        print(payload["sign"])

        payload["event"] = json.dumps(event)

        print((self.API_KEY + self.API_SECRET_KEY + json.dumps(event)))
        response = requests.post(url, payload)
        print(response.text)
        if response.status_code != 200:
            raise ShinyError('Network error:' + str(response.status_code))

    @staticmethod
    def recent():
        """获取最新项目"""
        url = config.API_HOST + '/Data/recent'
        response = requests.get(url)
        if response.status_code != 200:
            raise ShinyError('Network error:' + str(response.status_code))
        return json.loads(response.text)
# coding=utf-8
import json
import logging
from time import sleep

import requests


class PrivateApi:
    headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}

    def __init__(self, api_url):
        self.api_url = api_url
        self.max_retries = 10

    def submit(self, task):
        """
        :type task: Task
        """
        if self.api_url == 'http://STUB_URL':
            logging.info(u'DEV MODE Задача условно поставлена')
            return

        url = self.api_url + '/services/' + task.serviceId + '/tasks'
        last_e = None
        for idx in range(self.max_retries):
            try:
                return requests.post(
                    url=url,
                    data=json.dumps(task.__dict__),
                    headers=self.headers,
                    timeout=3
                )
            except requests.exceptions.ConnectionError as e:
                # При ошибках подключения пытаемся еще раз
                last_e = e
                sleep(1)
        raise last_e


#!/usr/bin/env python
# -*- coding: utf-8 -*-

from concurrent import futures
from multiprocessing import cpu_count
import requests
import logging

executor = futures.ProcessPoolExecutor(max_workers=cpu_count())


def _save(endpoint, token, agent, log, extra):
    headers = dict()
    headers["X-LOGCENTRAL-TOKEN"] = token
    headers["User-Agent"] = agent
    for k, v in extra.items():
        headers[k] = v

    res = requests.post(endpoint, data=log, headers=headers)
    if res.status_code != 200:
        logging.error("Fail to save log:%s:%s" % (str(res.status_code), str(res.content)))

    return True


def log(endpoint, token, agent, log, extra=None):
    f = executor.submit(_save, endpoint=endpoint, token=token, agent=agent, log=log, extra=extra)

    def callback(future):
        if future.exception():
            logging.error(future.exception())

    f.add_done_callback(callback)

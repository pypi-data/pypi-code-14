# -*- coding: utf-8 -*-
from __future__ import absolute_import
from rq import Connection, Worker
from redis import Redis
from os import getenv


def start_worker():
    from . import worker
    redis_host = getenv('REDIS_HOST', '127.0.0.1')
    redis_port = int(getenv('REDIS_PORT', '6379'))
    redis_db = int(getenv('REDIS_DB', '0'))

    with Connection(Redis(host=redis_host, port=redis_port, db=redis_db)):
        Worker(['default']).work()

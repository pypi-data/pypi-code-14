# -*- coding:utf-8 -*-
from .custom_redis_server import CustomRedis


def start_server():
    cr = CustomRedis.parse_args()
    cr.set_logger()
    cr.start()
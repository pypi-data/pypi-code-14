import os
import logging
import tornado.log

default_level = 'WARNING'

channel = logging.StreamHandler()
channel.setFormatter(tornado.log.LogFormatter(color=False))

logger = logging.getLogger()
logger.addHandler(channel)

logger.setLevel(
    logging.getLevelName(
        os.environ.get('LOGGER_LEVEL', default_level).upper()))

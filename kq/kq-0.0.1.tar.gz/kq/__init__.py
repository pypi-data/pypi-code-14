from __future__ import absolute_import, print_function, unicode_literals

import logging

from kq.decorators import job
from kq.exceptions import (
    WorkerInitError,
    QueueInitError
)
from kq.worker import Worker
from kq.queue import Queue
from kq.version import VERSION

__all__ = ['Worker', 'Queue', 'job', 'VERSION']

# Suppress noise from PyKafka
for logger_name in [
    'pykafka',
    'pykafka.rdkafka',
    'pykafka.connection',
    'pykafka.topic',
    'pykafka.simpleconsumer'
]:
    logger = logging.getLogger(logger_name)
    logger.propagate = False

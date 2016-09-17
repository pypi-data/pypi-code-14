import logging
import socket
from logging import StreamHandler
import sys

class ContextFilter(logging.Filter):
    hostname = socket.gethostname()
    svc_name = None

    def __init__(self, svc_name):
        self.svc_name = svc_name

    def filter(self, record):
        record.hostname = ContextFilter.hostname
        record.svc_name = self.svc_name
        return True

def getLogger(svc_name='test', level=logging.INFO):
    logger = logging.getLogger('k8s_logger_' + svc_name)
    logger.setLevel(level)

    f = ContextFilter(svc_name)
    logger.addFilter(f)

    handler = StreamHandler(sys.stdout)
    formatter = logging.Formatter('{"name": "%(svc_name)s", "msg": "%(message)s", "timestamp": "%(asctime)s.%(msecs)03dZ", "hostname": "%(hostname)s"}', datefmt='%Y-%m-%dT%H:%M:%S')

    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger

def getTracker(svc_name='test', level=logging.INFO):
    logger = logging.getLogger('k8s_metrics_tracker_' + svc_name)
    logger.setLevel(level)

    f = ContextFilter(svc_name)
    logger.addFilter(f)

    handler = StreamHandler(sys.stdout)
    formatter = logging.Formatter('{"type": "%(svc_name)s", "msg": {"value": "%(message)s"}, "date": "%(asctime)s.%(msecs)03dZ", "hostname": "%(hostname)s", "buffermetrics": true}', datefmt='%Y-%m-%dT%H:%M:%S')

    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger

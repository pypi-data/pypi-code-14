import logging
import socket
from logging import StreamHandler
import sys
from fluent import handler as fluent_handler
import json

log_custom_format = {
    "name": "%(svc_name)s",
    "msg": "%(message)s",
    "timestamp": "%(asctime)s.%(msecs)03dZ",
    "hostname": "%(hostname)s"
}

metric_custom_format = {
    "type": "%(svc_name)s",
    "value": "%(message)s",
    "date": "%(asctime)s.%(msecs)03dZ",
    "hostname": "%(hostname)s",
    "buffermetrics": "true"
}

class ContextFilter(logging.Filter):
    hostname = socket.gethostname()
    svc_name = None

    def __init__(self, svc_name):
        self.svc_name = svc_name

    def filter(self, record):
        record.hostname = ContextFilter.hostname
        record.svc_name = self.svc_name
        return True

def getLogger(svc_name='test', output='stdout', level=logging.INFO):
    logger = logging.getLogger('k8s_logger_' + svc_name)
    logger.setLevel(level)

    f = ContextFilter(svc_name)
    logger.addFilter(f)

    if output == 'td-agent-forward':
        handler = fluent_handler.FluentHandler('application.logs', host='log-aggregator-service.default', port=24224)
        formatter = fluent_handler.FluentRecordFormatter(log_custom_format, datefmt='%Y-%m-%dT%H:%M:%S')
    else:
        handler = StreamHandler(sys.stdout)
        formatter = logging.Formatter(json.dumps(log_custom_format), datefmt='%Y-%m-%dT%H:%M:%S')

    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger

def getTracker(svc_name='test', output='stdout', level=logging.INFO):
    logger = logging.getLogger('k8s_metrics_tracker_' + svc_name)
    logger.setLevel(level)

    f = ContextFilter(svc_name)
    logger.addFilter(f)

    if output == 'td-agent-forward':
        handler = fluent_handler.FluentHandler('application.metrics', host='log-aggregator-service.default', port=24224)
        formatter = fluent_handler.FluentRecordFormatter(metric_custom_format, datefmt='%Y-%m-%dT%H:%M:%S')
    else:
        handler = StreamHandler(sys.stdout)
        formatter = logging.Formatter(json.dumps(metric_custom_format), datefmt='%Y-%m-%dT%H:%M:%S')

    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger

from datetime import datetime
import functools
import logging
import sys
from time import time

import six

from .messages import Notification
from .messages import Request


logger = logging.getLogger('mushroom.rpc.middleware')


class Middleware(object):

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)


class MiddlewareStack(object):

    def __init__(self, middlewares, get_response):
        self.get_response = get_response
        for m in reversed(middlewares):
            self.get_response = m(self.get_response)

    def __call__(self, request):
        return self.get_response(request)


class SlowMethodLogMiddleware(Middleware):
    '''
    Default thresholds:
    (10, 'error'), (1, 'warning')
    '''

    def __init__(self, get_response, thresholds=None):
        super(SlowMethodLogMiddleware, self).__init__(get_response)
        if thresholds is None:
            self.thresholds = [(10, 'error'), (1, 'warning')]
        else:
            self.thresholds = list(thresholds)
            self.thresholds.sort(reverse=True)

    def __call__(self, request):
        request.start_time = time()
        try:
            return super(SlowMethodLogMiddleware, self).__call__(request)
            self.log_if_slow(request, 'Slow method "%s" returned normally after %.3fs')
        except:
            self.log_if_slow(request, 'Slow method "%s" returned an error after %.3fs')
            raise

    def log_if_slow(self, request, message):
        duration = time() - request.start_time
        for threshold, log_level in self.thresholds:
            if duration > threshold:
                log_args = (message, request.method, duration)
                log_method = getattr(logger, log_level)
                log_method(*log_args)
                break


class StatisticsMiddleware(Middleware):

    def __call__(self, request):
        request.session.last_activity = datetime.now()
        request.session.message_count = getattr(request.session, 'message_count', 0) + 1
        return super(StatisticsMiddleware, self).__call__(request)

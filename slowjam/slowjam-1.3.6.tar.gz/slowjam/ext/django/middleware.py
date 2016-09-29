try:
    from django.conf import settings
except ImportError:
    class Settings(object):
        SLOWJAM_LOG_THRESHOLD = 200

    settings = Settings()

try:
    from django.utils.deprecation import MiddlewareMixin
except ImportError:
    MiddlewareMixin = object

import json
import logging
import time

from slowjam.context import slowjam_context
from slowjam.statsd_client import graphite_duration, graphite_increment
logger = logging.getLogger(__name__)


class RequestTimerMiddleware(MiddlewareMixin):
    def process_view(self, request, view_func, view_args, view_kwargs):
        t = time.time()
        try:
            key = 'HTTP_X_QUEUE_START'
            queue_time = float(request.META[key])
        except:
            queue_time = t

        request._logging_ctx = {'start_time': t, 'queue_time': queue_time}

    def process_response(self, request, response):
        ctx = getattr(request, '_logging_ctx', None)
        if ctx:
            start_time = ctx['start_time']
            queue_time = ctx['queue_time']
            end_time = time.time()
            queue_time_ms = (start_time - queue_time) * 1000
            request_time_ms = (end_time - start_time) * 1000
            host_name = 'localhost'

            if request_time_ms > 20 or queue_time_ms > 20:
                redirect_url = 'dest=%s' % response['Location'] if response.status_code in (301, 302) else ''
                logger.info('Request took %.4fms (queue=%.4fms): request_id=%s remote_ip=%s method=%s host=%s, url=%s, status=%d%s',
                            request_time_ms, queue_time_ms, getattr(request, 'id', None), request.META.get('REAL_IP'),
                            request.method, host_name, request.get_full_path(), response.status_code, redirect_url)

            graphite_duration('queue_duration.all', queue_time_ms)
            graphite_duration('request_duration.all', request_time_ms)
            graphite_increment('request_count.all')

            if response.status_code > 399 and response.status_code < 600:
                graphite_increment('request_count.%d' % response.status_code)
                graphite_increment('request_count.hosts.%s.%d' % (host_name, response.status_code))

        return response

class SlowjamMiddleware(MiddlewareMixin):

    @staticmethod
    def log_time(*args, **kwargs):
        return graphite_duration(*args, **kwargs)

    def process_view(self, request, view_func, view_args, view_kwargs):
        try:
            request.view_name = '.'.join((view_func.__module__, view_func.__name__))
        except AttributeError:
            request.view_name = '(unknown)'

        t = time.time()
        try:
            key = 'HTTP_X_QUEUE_START'
            queue_time = float(request.META[key])
        except:
            queue_time = t

        request._logging_ctx = {'start_time': t, 'queue_time': queue_time}

        if slowjam_context:
            extras = {
                'host': request.META.get('HTTP_HOST'),
                'ip': request.META.get('REAL_IP'),
                'method': request.method,
                'uri': request.get_full_path(),
                'view': request.view_name,
                'view_args': view_args,
                'view_kwargs': view_kwargs,
            }

            slowjam_context.start('request', extras=extras, time_recorder=self.log_time)

    def process_response(self, request, response):
        if slowjam_context:
            profile = slowjam_context.stop()
            if profile:
                exec_time = profile.execution_time
                if exec_time and exec_time > getattr(settings, 'SLOWJAM_LOG_THRESHOLD', 200):
                    if settings.DEBUG:
                        # Here you might want to blacklist certain kinds of views from showing up
                        if profile:
                            print ''
                            print unicode(profile)
                            print ''
                    else:
                        d = profile.to_dict()
                        serialized_profile = json.dumps(d, separators=(',', ':'))
                        logger.info('slowjam', extra={'slowjam': serialized_profile})

        return response

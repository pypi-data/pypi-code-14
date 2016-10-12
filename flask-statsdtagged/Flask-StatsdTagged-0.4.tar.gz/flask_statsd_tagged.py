import re
import time
import sys
import socket
import resource
from flask import request, g
from flask import _app_ctx_stack as stack
from statsd import StatsClient


def add_tags(metric, **tags):
    if not metric:
        return metric
    tag_str = ','.join([('%s=%s' % (k, v)) for k, v in tags.items()])
    return '%s,%s' % (metric, tag_str)

def _get_context_tags():
    try:
        return g.statsd_tags
    except AttributeError:
        return {}


class FlaskStatsdTagged(object):

    def __init__(self, app=None, host='localhost', port=8125, extra_tags={}):
        self.app = app
        self.hostname = socket.gethostname()
        self.statsd_host = host
        self.statsd_port = port
        self.extra_tags = extra_tags
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        app.before_request(self.before_request)
        app.after_request(self.after_request)
        self.connection = self.connect()

    def connect(self):
        return StatsClient(host=self.statsd_host,
                           port=self.statsd_port,
                           maxudpsize=1024)

    def before_request(self):
        ctx = stack.top
        ctx.request_begin_at = time.time()
        ctx.resource_before = resource.getrusage(resource.RUSAGE_SELF)

    def after_request(self, resp):
        ctx = stack.top
        period = (time.time() - ctx.request_begin_at) * 1000
        rusage = resource.getrusage(resource.RUSAGE_SELF)

        tags = dict(self.extra_tags)
        tags.update({"path":request.path or "notfound", "server": self.hostname, "status_code": resp.status_code})
        tags.update(_get_context_tags())
        with self.pipeline() as pipe:
            flaskrequest = add_tags("flaskrequest", **tags)
            pipe.incr(flaskrequest)
            pipe.timing(flaskrequest, period)

            # NOTE: The resource-based timing will (probably) only be relevant if each flask request
            # is handled by a single process, i.e. no threads.

            pipe.timing(add_tags("flask_usertime", **tags), 1000 * (rusage.ru_utime - ctx.resource_before.ru_utime))
            pipe.timing(add_tags("flask_systime", **tags), 1000 * (rusage.ru_stime - ctx.resource_before.ru_stime))

            pipe.incr(add_tags("flask_request_datasize", **tags), len(request.data))

        return resp

    def pipeline(self):
        return self.connection.pipeline()

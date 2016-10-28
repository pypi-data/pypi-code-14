import contextlib
import datetime.datetime
import tornado.gen
import statsd


class Client(object):
    def __init__(self, statsd_url, namespace):
        ip, port = statsd_url.split(':')
        self.client = statsd.StatsClient(ip, port=int(port), prefix=namespace)

    def timing(name, duration):
        pass

    @contextlib.contextmanager
    def instrument_manager(self, name):
        def send_duration():
            duration = (datetime.datetime.now() - start).total_seconds()
            self.timing("{}.duration".format(name),
                               int(duration * 1000))

        start = datetime.datetime.now()

        try:
            yield
        except Exception as e:
            self.incr('{}.exceptions.{}'.format(name, e.__class__.__name__))
            send_duration()

            raise e
        else:
            self.incr('{}.success'.format(name))
            send_duration()

    def instrument_decorator(self, name):
        def instrument_wrapper(fn):
            @tornado.gen.coroutine
            def fn_wrapper(*args, **kwargs):
                with self.instrument_wrapper(name):
                    result = yield tornado.gen.maybe_future(
                        fn(*args, **kwargs))
                    raise tornado.gen.Return(result)

            return fn_wrapper
        return instrument_wrapper

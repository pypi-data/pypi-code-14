''''''

import resource

from tornado import gen


class ResourceReporter:
    
    sleep_time = 10
    '''Send reports per given number of seconds'''

    _ioloop = None
    '''Tornado IO loop'''
    
    _statsd = None
    '''Metrics client'''
    
    _prefix = None
    '''Stasd gauge prefix for worker processes monitoring'''
    
    _running = None
    '''Running flag'''
    
    _last_cpu_time = None
    '''Used CPU time form previous iteration'''
    
    
    def __init__(self, ioloop, statsd, prefix='process'):
        self._ioloop = ioloop
        self._statsd = statsd
        self._prefix = prefix
    
    @gen.coroutine
    def _worker(self):
        while self._running:
            usage = resource.getrusage(resource.RUSAGE_SELF)
            with self._statsd.pipeline() as pipe:
                cpu_usage = usage.ru_utime + usage.ru_stime
                if self._last_cpu_time is not None:
                    pipe.gauge('{}.cpu'.format(self._prefix), 
                        (cpu_usage - self._last_cpu_time) / self.sleep_time)
                self._last_cpu_time = cpu_usage
                    
                pipe.gauge('{}.rss'.format(self._prefix), usage.ru_maxrss)
                
                pipe.gauge('{}.ioloop.handler'.format(self._prefix),  
                    len(self._ioloop._handlers or ()))
                pipe.gauge('{}.ioloop.callback'.format(self._prefix), 
                    len(self._ioloop._callbacks or ()))
                pipe.gauge('{}.ioloop.timeout'.format(self._prefix),
                    len(self._ioloop._timeouts or ()))
                
            yield gen.sleep(self.sleep_time)
    
    def start(self):
        self._running = True
        self._ioloop.add_callback(self._worker)
    
    def stop(self):
        self._running = False


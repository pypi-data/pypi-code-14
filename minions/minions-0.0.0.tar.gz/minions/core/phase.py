import os
import random
import gevent
import logging
import traceback
import coloredlogs
import multiprocessing
import zmq.green as zmq
from agentzero.core import SocketManager

logger = logging.getLogger('phase')


class Phase(object):
    def __init__(self, id):
        self.id = ".".join(map(bytes, [os.getpid(), id]))
        self.context = zmq.Context()
        self.sockets = SocketManager(zmq, self.context)
        self.sockets.create('jobs_in', zmq.REQ)
        self.sockets.set_socket_option('jobs_in', zmq.SNDHWM, 1)
        self.sockets.set_socket_option('jobs_in', zmq.RCVHWM, 1)
        self.socket_identity = b'.'.join([self.name, bytes(self.id)])
        self.sockets.set_socket_option('jobs_in', zmq.IDENTITY, self.socket_identity)
        self.processed_jobs = []

    @property
    def name(self):
        return self.__class__.__name__

    def request_job(self):
        data = {
            'phase': self.to_dict(),
        }
        if len(self.processed_jobs) > 0:
            last_job = self.processed_jobs.pop(0)
            data['last_job'] = last_job

        sent = self.sockets.send_safe('jobs_in', data, polling_timeout=-1)
        if sent:
            return self.sockets.recv_safe('jobs_in', polling_timeout=-1)

    def connect(self):
        self.sockets.connect('jobs_in', 'tcp://127.0.0.1:3000', zmq.POLLIN | zmq.POLLOUT)

    def reconnect(self):
        self.connect()
        gevent.sleep(2)

    def process_job(self, job):
        arguments = job['arguments']
        try:
            result = self.execute(**arguments) or {}
            logger.info('%s %s success', self.name, self.id)
        except Exception as e:
            result = {
                'error': traceback.format_exc(e),
            }
            logger.error('%s %s failed', self.name, self.id)

        self.processed_jobs.append(result)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name
        }

    def loop_once(self):
        job = self.request_job()
        if isinstance(job, dict):
            self.process_job(job)

        else:
            self.reconnect()

        logger.debug("phase %s [%s] loop", self.name, self.id)

    def run(self):
        logger.info('%s is running', self.name)
        self.connect()

        while True:
            self.loop_once()


class RandomGenerator(Phase):
    def execute(self, size, encoding):
        gevent.sleep(random.choice([i / 1000.0 for i in range(1, 11)]))
        return {
            'result': os.urandom(int(size)).encode(bytes(encoding))
        }


class StringReverser(Phase):
    def execute(self, string):
        gevent.sleep(random.choice([i / 500.0 for i in range(1, 11)]))
        return {
            'result': "".join(list(reversed(string)))
        }


def main():
    import gevent.monkey
    from gevent.pool import Pool
    coloredlogs.install(level=logging.INFO)
    gevent.monkey.patch_all()
    size = multiprocessing.cpu_count()
    pool = Pool(size)
    for index in range(1, size + 1):
        pool.spawn(RandomGenerator(index).run)
        pool.spawn(StringReverser(index).run)

    pool.join(raise_error=True)


if __name__ == '__main__':
    main()

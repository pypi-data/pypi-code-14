from __future__ import absolute_import, print_function, unicode_literals

import logging
import time
try:
    import cPickle as pickle
except ImportError:
    import pickle

from pykafka import KafkaClient

from kq.exceptions import (
    QueueInitError,
    JobEnqueueError
)
from kq.utilities import to_str

logger = logging.getLogger(__name__)


class Queue(object):

    def __init__(self,
                 hosts=None,
                 topic=None,
                 sync=False,
                 timeout=None,
                 rdkafka=False):
        """Initialize the Kafka queue.

        :param hosts: Kafka host names and ports
        :param hosts: list
        :param topic: the name of the target topic
        :type topic: str
        :param sync: save failed jobs synchronously
        :type sync: bool
        :param timeout: the job timeout threshold in seconds
        :type timeout: int
        :param rdkafka: enqueue jobs using librdkafka
        :type rdkafka: bool
        """
        self._hosts = hosts or ['127.0.0.1:9092']
        self._client = KafkaClient(b','.join(self._hosts))
        self._topic = topic or 'default'
        self._sync = sync
        self._timeout = timeout
        self._rdkafka = rdkafka

        if not isinstance(self._client, KafkaClient):
            raise QueueInitError('Invalid Kafka client')

        if self._topic.encode('utf-8') not in self._client.topics:
            raise QueueInitError('Topic "{}" not found'.format(self._topic))

        # Initialize the job producer for the topic
        self._producer = self._client.topics[
            self._topic.encode('utf-8')
        ].get_producer(
            auto_start=True,
            delivery_reports=False,
            sync=self._sync,
            use_rdkafka=self._rdkafka
        )

    def __del__(self):
        """Stop the producer for the target topic."""
        if hasattr(self, '_producer'):
            self._producer.stop()

    def __repr__(self):
        """Return a string representation of the queue.

        :return: the string representation
        :rtype: str
        """
        return 'Queue(topic: {})'.format(self._topic)

    @property
    def hosts(self):
        """Return the Kafka host names and ports.

        :return: Kafka host names and ports
        :rtype: list
        """
        return self._hosts

    @property
    def client(self):
        """Return the Kafka client.

        :return: the Kafka client
        :rtype: pykafka.KafkaClient
        """
        return self._client

    @property
    def topic(self):
        """Return the queue name.

        :return: the queue name
        :rtype: str
        """
        return self._topic

    @property
    def sync(self):
        """Check whether jobs are enqueued synchronously.

        :return: `True` if jobs are enqueued synchronously, else `False`
        :rtype: bool
        """
        return self._sync

    @property
    def rdkafka(self):
        """Check whether librdkafka is in use or not.

        :return: `True` if librdkafka is in use, else `False`
        :rtype: bool
        """
        return self._rdkafka

    @property
    def timeout(self):
        """Return the job timeout threshold in seconds.

        If timeout is not set, the job will execute until it terminates.

        :return: the job timeout threshold in ms
        :rtype: int or None
        """
        return self._timeout

    def enqueue(self, func, *args, **kwargs):
        """Serialize the function call and place it in the Kafka topic.

        :param func: the function to enqueue
        :type func: callable
        :param args: the function arguments
        :type args: list
        :param kwargs: the function keyword arguments
        :type kwargs: dict
        :raises kq.exceptions.JobEnqueueError: on invalid argument
        """
        if not callable(func):
            raise JobEnqueueError('Excepting a callable')
        job_data = {
            'timestamp': int(time.time()),
            'timeout': self._timeout,
            'topic': self._topic,
            'func': func,
            'args': args,
            'kwargs': kwargs
        }
        self._producer.produce(pickle.dumps(job_data))
        logger.info('Enqueued job: {}'.format(to_str(func, args, kwargs)))

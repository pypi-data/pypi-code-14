from __future__ import absolute_import, print_function, unicode_literals

import logging
import multiprocessing
try:
    import cPickle as pickle
except ImportError:
    import pickle

from pykafka import KafkaClient, exceptions

from kq.exceptions import WorkerInitError
from kq.utilities import to_str

logger = logging.getLogger(__name__)


class Worker(object):
    """Kafka worker class."""

    def __init__(self,
                 hosts=None,
                 topic=None,
                 sync=False,
                 timeout=None,
                 rdkafka=False):
        """Initialize the Kafka worker.

        :param hosts: Kafka host names and ports
        :param hosts: list
        :param topic: the name of the target topic
        :type topic: str
        :param sync: save failed jobs synchronously
        :type sync: bool
        :param timeout: the job timeout threshold in seconds
        :type timeout: int
        :param rdkafka: quarantine failed jobs using librdkafka
        :type rdkafka: bool
        """
        self._hosts = hosts or ['127.0.0.1:9092']
        self._client = KafkaClient(b','.join(self._hosts))
        self._topic = topic or 'default'
        self._sync = sync
        self._timeout = timeout
        self._rdkafka = rdkafka
        self._pool = multiprocessing.Pool(processes=1)

        if self._topic.encode('utf-8') not in self._client.topics:
            raise WorkerInitError('Topic "{}" not found'.format(self._topic))
        if b'quarantine' not in self._client.topics:
            raise WorkerInitError('Topic "quarantine" not found')

        # Initialize the job consumer for the target topic
        self._consumer = self._client.topics[
            self._topic.encode('utf-8')
        ].get_balanced_consumer(
            consumer_group=self._topic.encode('utf-8'),
            managed=True,
            auto_commit_enable=True,
            consumer_timeout_ms=-1,
        )
        # Initialize the producer for the quarantine topic
        self._quarantine = self._client.topics[
            b'quarantine'
        ].get_producer(
            auto_start=True,
            delivery_reports=False,
            sync=self._sync,
            use_rdkafka=self._rdkafka
        )

    def __del__(self):
        """Commit the consumer offsets and stop the quarantine producer."""
        if hasattr(self, '_consumer'):
            try:
                logger.info('Committing consumer offsets ...')
                self._consumer.commit_offsets()
            except Exception as err:
                logger.exception(
                    'Failed to commit consumer offsets: {}'.format(err))
        if hasattr(self, '_quarantine'):
            try:
                logger.info('Stopping the quarantine producer ...')
                self._quarantine.stop()
            except Exception as err:
                logger.exception(
                    'Failed to stop the quarantine producer: {}'.format(err))

    def __repr__(self):
        """Return a string representation of the worker.

        :return: the string representation
        :rtype: str
        """
        return 'Worker(topic: {})'.format(self._topic)

    def _execute_func(self, func, args, kwargs, timeout=None):
        """Execute the given function with a timeout.

        :param func: the function to execute
        :type func: callable
        :param args: the arguments
        :type args: dict
        :param kwargs: the keyword arguments
        :type kwargs: dict
        :param timeout: the timeout threshold
        :type timeout: int
        :return: the result of the execution
        :rtype: object
        """
        timeout = timeout or self._timeout
        if timeout is None:
            return func(*args, **kwargs)
        else:
            result = self._pool.apply_async(func, args, kwargs)
            return result.get(timeout)

    def _consume_jobs(self):
        for job in self._consumer:
            offset, raw_job_data = job.offset, job.value
            try:
                job_data = pickle.loads(raw_job_data)
                timeout = job_data['timeout']
                func = job_data['func']
                args = job_data['args']
                kwargs = job_data['kwargs']
            except Exception as err:
                logger.exception(
                    'Job {} failed to load: {}'.format(offset, err))
                self._quarantine.produce(raw_job_data)
            else:
                try:
                    logger.info('Executing job {}: {} ...'.format(
                        offset, to_str(func, args, kwargs)))
                    res = self._execute_func(func, args, kwargs, timeout)
                except multiprocessing.TimeoutError:
                    logger.error(
                        'Job {} timed out ({}s)'.format(offset, timeout))
                    self._quarantine.produce(job.value)
                except Exception as err:
                    logger.exception(
                        'Job {} failed to run: {}'.format(offset, err))
                    self._quarantine.produce(job.value)
                else:
                    logger.info(
                        'Job {} returned: {}'.format(offset, repr(res)))

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
        """Return the name of the target topic.

        :return: the name of the target topic
        :rtype: str
        """
        return self._topic

    @property
    def sync(self):
        """Check whether failed jobs are quarantined synchronously.

        :return: `True` if the quarantine is synchronous, else `False`
        :rtype: bool
        """
        return self._sync

    @property
    def rdkafka(self):
        """Check whether *librdkafka* is in use or not.

        :return: `True` if *librdkafka* is in use, else `False`
        :rtype: bool
        """
        return self._rdkafka

    @property
    def timeout(self):
        """Return the job timeout threshold in seconds.

        .. note:

            The timeout defined during the job enqueue is overridden.

        :return: the job timeout threshold in seconds
        :rtype: int
        """
        return self._timeout

    def start(self):
        """Start running the enqueued jobs.

        Any jobs that cannot be loaded or executed are automatically sent
        to the "quarantine" topic.
        """
        logger.info('Starting {} ...'.format(self))
        while True:
            try:
                self._consume_jobs()
            except exceptions.UnknownMemberId:
                # When the member ID is missing, sleep and try again
                pass

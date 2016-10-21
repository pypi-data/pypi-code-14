from __future__ import absolute_import, print_function, unicode_literals

from functools import wraps

from kq.exceptions import JobDecoratorError
from kq.queue import Queue


def job(queue):
    """A decorator which adds a **delay** method to the decorated function.

    When the **delay** method is called, the function is enqueued as a job.
    For example:

    .. code-block:: python

        client = pykafka.KafkaClient(hosts='localhost:9092')
        default_queue = Queue(client=client, topic='default')

        @job(default_queue)
        def add_numbers(a, b):
            return a + b

        add_numbers.delay(1, 2) # Put the function into topic 'default'

    :param queue: The queue instance
    :type queue: kq.queue.Queue
    :return: the job decorator
    :rtype: callable
    """
    if not isinstance(queue, Queue):
        raise JobDecoratorError('Invalid queue instance')

    def decorator(func):

        @wraps(func)
        def delay(*args, **kwargs):
            queue.enqueue(func, *args, **kwargs)
        func.delay = delay
        return func

    return decorator

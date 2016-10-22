from tornado.ioloop import IOLoop
from tornado import concurrent

from tornado_retry.engine import RetryEngine, TooManyAttempts
from tornado_retry import backoff as _backoff, jitter as _jitter
from tornado_retry import log

from tornado_retry.__about__ import *  # noqa

__all__ = [
    'retry',
    'TooManyAttempts',
]


def retry(func, min_delay=0, max_delay=60, max_retries=5,
          backoff='exponential', jitter='full', on_error=None,
          on_schedule=None, ioloop=None, logger=None):
    """
    Retry `func` until it either succeeds or `max_retries` is hit.

    Typical usage:
        from functools import partial
        from tornado import gen, httpclient
        from tornado_retry import retry

        @gen.coroutine
        def get_server_data(url):
            http_client = httpclient.AsyncHTTPClient()

            response = yield retry(partial(http_client.fetch, url))

            raise gen.Return(response)

    :param func: The function to be called with no args. If the function
        fails (aka raises an exception) then it is retried.
    :param min_delay: The minimum amount of time in seconds to wait before
        retrying the function.
    :param max_delay: The maximum amount of time in seconds to wait before
        retrying the function.
    :param max_retries: The maximum number of time to retry the function. If
        all calls to the function fail then :ref:`TooManyAttempts` will be
        raised.
    :param backoff: Strategy to use to determine how much delay in seconds to
        wait before retrying the function. See :ref:`_backoff.backoff`.
    :param jitter: Strategy to use to determine how much jitter to apply to the
        delay before retrying the function. See :ref:`_jitter.jitter`.
    :param on_error: If supplied, called when an attempt to call :ref:`func`
        fails. The only argument that is supplied is the `sys.exc_info()` tuple
        that will contain the exception that was raised in the attempt. This
        function provides an opportunity to the user to conditionally short
        circuit the retry loop by returning a `True` or `False` value
        indicating whether the loop should continue. By default the loop will
        continue no matter what exception is raised.
    :param on_schedule: If supplied, called when an attempt to call the
        function is scheduled for a future time. Two arguments are supplied:
        The number of attempts that have been made to call function (an
        integer) and the number of seconds in the future that the attempt has
        been scheduled for. This is mostly useful for logging and other user
        notifications.
    :param ioloop: Supply your own :ref:`IOLoop` if needed. By default, the
        current installed loop is used.
    :param logger: By default, all retry logging goes to the `tornado_retry`
        logger. Switch this if you want.
    :returns: A :ref:`concurrent.Future` that will hold either the result or
        last exception that occurred while running the loop.
    """
    ioloop = ioloop or IOLoop.current()
    future = concurrent.Future()

    delay_iter = _backoff.get_iter(backoff, max_delay)
    jitter_func = _jitter.jitter(jitter)
    backoff_iter = _backoff.backoff(
        delay_iter,
        jitter_func,
        min_delay,
        max_delay,
        max_retries
    )

    engine = RetryEngine(
        func,
        backoff_iter,
        on_success=lambda result: future.set_result(result),
        on_failure=lambda exc_info: future.set_exc_info(exc_info),
        on_error=on_error,
        on_schedule=on_schedule,
        logger=logger or log.logger,
        call_later=ioloop.call_later,
    )

    engine.start()

    return future

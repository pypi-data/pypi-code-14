import sys

from tornado.ioloop import IOLoop
from tornado import gen


__all__ = [
    'TooManyAttempts',
    'RetryEngine',
]


class TooManyAttempts(Exception):
    """
    Raised when the loop exits because too many attempts to retry were made.
    """


class RetryEngine(object):
    """
    :ivar func: The function to call on each retry.
    :ivar delay_iter: An iterable that provides the number of seconds to
        backoff if a failure occurs.
    :ivar on_success: If at any point `func` succeeds, this will be called with
        it's result as the first argument.
    :ivar on_failure: Called when the retry loop is dead. Will be given the
        `exc_info` provided as a tuple (`on_failure(sys.exc_info())`) with the
        exception that killed the loop.
    :ivar on_error: If the call to `func` raises an exception, this will be
        called to provide a user the ability to decide whether to continue
        retrying the loop. The handler will be give the `exc_info` provided as
        a tuple (`on_error(sys.exc_info())`). This function should return
        `True` to continue with the retry loop or.
    :ivar on_schedule: When the retry loop is scheduled, this callback will be
        fired with the args (attempt, delay). `attempt` is the number of times
        that the loop has fired, `delay` is the number of seconds that will be
        waited before the loop will run.
    :ivar logger: A `logging.Logger` instance that will provide useful
        information from time to time. If not provided, the module level logger
        will be used.
    :ivar call_later: Function that will schedule the next attempt in the
        scheduler. If this is not supplied, the current ioloop will be used.
    :ivar tries: The number of times that an attempt to call `func` has been
        made.
    """

    def __init__(self, func, delay_iter, on_success, on_failure, on_error,
                 on_schedule, logger, call_later=None):
        self.func = func
        self.delay_iter = delay_iter
        self.on_success = on_success
        self.on_failure = on_failure
        self.on_error = on_error
        self.on_schedule = on_schedule

        if not call_later:
            call_later = IOLoop.current().call_later

        self.call_later = call_later
        self.logger = logger
        self.tries = 0

    def do_attempt(self):
        """
        Perform the actions necessary to call func and handle any error/success
        gracefully.
        """
        self.tries += 1

        try:
            result = self.func()
        except:
            self.handle_exception(sys.exc_info())

            return

        attempt_future = gen.maybe_future(result)

        attempt_future.add_done_callback(self.handle_attempt)

    def handle_attempt(self, future):
        """
        This is the callback that is made when the attempt to call :ref:`func`
        is made.

        Note that is important that this method does not raise any exceptions.

        :param future: The `concurrent.Future` that holds the result of the
            call to :ref:`func`.
        """
        exc_info = future.exc_info()

        if not exc_info:
            self.handle_result(future.result())

            # the function succeeded without exception, kill the loop
            return

        self.handle_exception(exc_info)

    def handle_result(self, result):
        """
        When the call to `func` succeeds, this will be called to report the
        result.

        Note that is important that this method does not raise any exceptions.

        :param result: The return of the call to `func`.
        """
        try:
            self.on_success(result)
        except:
            self.handle_failure(sys.exc_info())

    def should_retry(self, exc_info):
        """
        If an exception occurs while attempting to retry the func, decide
        whether the retry loop should continue.

        :param exc_info: The `sys.exc_info` of the exception caused by calling
            `func`.
        """
        if not self.on_error:
            return True

        return bool(self.on_error(exc_info))

    def handle_exception(self, exc_info):
        """
        An exception occurred when calling `func`. Provide the ability to
        recover and continue retrying via the `on_error` callback.

        Note that is important that this method does not raise any exceptions.

        :param exc_info: The `sys.exc_info` of the exception caused by calling
            `func`.
        """
        try:
            should_retry = self.should_retry(exc_info)
        except:
            self.logger.exception(
                'Error while checking if the loop should be retried',
                exc_info=exc_info,
            )
            self.handle_failure(sys.exc_info())

            return

        if not should_retry:
            self.handle_failure(exc_info)

            return

        try:
            self.next()
        except:
            self.handle_failure(exc_info)

    def handle_failure(self, exc_info):
        """
        If an error occurs then `on_failure` needs to be called with exception
        info. If the call to that fails, then the best we can do is log the
        exception so that it is as visible as possible.

        Note that is important that this method does not raise any exceptions.
        """
        try:
            self.on_failure(exc_info)
        except:
            self.logger.exception('Error caught from %r' % (self.on_failure,))
            self.logger.error('Original exception:', exc_info=exc_info)

    def next(self):
        """
        Perform the next iteration of the retry loop.

        Determine what the delay should be and then schedule it to run.
        """
        try:
            delay = self.delay_iter.next()
        except (StopIteration, GeneratorExit):
            self.handle_failure(
                (TooManyAttempts, TooManyAttempts(), None)
            )

            return
        except:
            self.handle_failure(sys.exc_info())

            return

        self.schedule_attempt(delay)

    def schedule_attempt(self, delay):
        """
        Schedule an attempt to run func in `delay` seconds time.
        """
        try:
            self.call_later(delay, self.do_attempt)

            if self.on_schedule:
                self.on_schedule(self.tries + 1, delay)
        except:
            self.handle_failure(sys.exc_info())

            return

    def start(self):
        if self.tries != 0:
            raise RuntimeError('Loop already started!')

        self.schedule_attempt(0)

    def __iter__(self):
        return self

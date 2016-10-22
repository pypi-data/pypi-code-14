"""
Integration level tests for retry.
"""

from tornado.testing import AsyncTestCase, gen_test
from tornado import concurrent
from tornado_retry import retry, TooManyAttempts


class TestError(Exception):
    pass


def sync_fail():
    raise TestError


def async_fail():
    future = concurrent.Future()

    future.set_exception(TestError)

    return future


def sync_succeed():
    return 'yay'


def async_succeed():
    future = concurrent.Future()

    future.set_result('yay')

    return future


class RetryTestCase(AsyncTestCase):
    @gen_test
    def test_sync_too_many_attempts(self):
        """
        Too many attempts to retry must raise :ref:`TooManyAttempts`.
        """
        with self.assertRaises(TooManyAttempts):
            yield retry(sync_fail, min_delay=0, max_delay=0, max_retries=3)

    @gen_test
    def test_async_too_many_attempts(self):
        """
        Too many attempts to retry must raise :ref:`TooManyAttempts`.
        """
        with self.assertRaises(TooManyAttempts):
            yield retry(async_fail, min_delay=0, max_delay=0, max_retries=3)

    @gen_test
    def test_sync_succeed(self):
        """
        Simple success functions done in a synchronous way works as expected.
        """
        result = yield retry(sync_succeed)

        self.assertEqual(result, 'yay')

    @gen_test
    def test_async_succeed(self):
        """
        Simple success functions done in an Asynchronous way works as expected.
        """
        result = yield retry(async_succeed)

        self.assertEqual(result, 'yay')


class OnScheduleTestCase(AsyncTestCase):
    @gen_test
    def test_sanity(self):
        self.count = 0

        def on_schedule(attempt, delay):
            if self.count == 0:
                self.assertEqual(attempt, 1)
                self.assertEqual(delay, 0.0)
            elif self.count == 1:
                self.assertEqual(attempt, 2)
                self.assertEqual(delay, 0.1)
            else:
                self.fail('Called to many times')

            self.count += 1

        with self.assertRaises(TooManyAttempts):
            yield retry(
                async_fail,
                on_schedule=on_schedule,
                max_retries=2,
                max_delay=0.1,
                jitter='none',
                backoff='exponential',
            )

        self.assertEqual(self.count, 2)

    @gen_test
    def test_exception(self):
        self.executed = False

        def on_schedule(attempt, delay):
            raise TestError

        with self.assertRaises(TestError):
            yield retry(sync_succeed, on_schedule=on_schedule)

    @gen_test
    def test_async_error(self):
        self.executed = False

        def on_schedule(attempt, delay):
            raise TestError

        with self.assertRaises(TestError):
            yield retry(async_succeed, on_schedule=on_schedule)


class ShouldRetryTestCase(AsyncTestCase):
    @gen_test
    def test_missing(self):
        """
        If no `on_error` handler is passed, the loop should retry indefinitely.
        """
        with self.assertRaises(TooManyAttempts):
            yield retry(sync_fail, min_delay=0, max_delay=0, max_retries=2)

    @gen_test
    def test_expected_error(self):
        """
        If a loop attempt fails with an expected error, the loop should
        continue.
        """
        def on_error(exc_info):
            return isinstance(exc_info[1], TestError)

        with self.assertRaises(TooManyAttempts):
            yield retry(
                sync_fail,
                min_delay=0,
                max_delay=0,
                max_retries=2,
                on_error=on_error,
            )

    @gen_test
    def test_unexpected_error(self):
        """
        If a loop attempt fails with an unexpected error, the loop should bail
        with raising the exception that the func caused.
        """
        def on_error(exc_info):
            return not isinstance(exc_info[1], TestError)

        with self.assertRaises(TestError):
            yield retry(
                sync_fail,
                min_delay=0,
                max_delay=0,
                on_error=on_error,
            )

    @gen_test
    def test_fail(self):
        """
        If an exception is raised in calling `on_error`, that exception should
        be raised.
        """
        class OnErrorException(Exception):
            pass

        def on_error(exc_info):
            raise OnErrorException

        with self.assertRaises(OnErrorException):
            yield retry(
                sync_fail,
                min_delay=0,
                max_delay=0,
                on_error=on_error,
            )

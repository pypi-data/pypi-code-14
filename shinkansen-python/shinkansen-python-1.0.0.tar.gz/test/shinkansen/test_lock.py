import mock
import unittest

import redlock.lock

from shinkansen import config, lock


class TestLock(unittest.TestCase):
    def setUp(self):
        super(TestLock, self).setUp()
        self.orig_QUEUE_SYSTEM = config.QUEUE_SYSTEM
        config.QUEUE_SYSTEM = 'celery'
        self.redlock = mock.patch.object(redlock.lock.ReentrantRedLock, '__init__', return_value=None).start()
        self.redlock_acquire = mock.patch.object(redlock.lock.ReentrantRedLock, 'acquire').start()
        self.redlock_release = mock.patch.object(redlock.lock.ReentrantRedLock, 'release').start()
        self.redlock_acquire.return_value = True

    def tearDown(self):
        mock.patch.stopall()
        config.QUEUE_SYSTEM = self.orig_QUEUE_SYSTEM

    def test_passthrough(self):
        test_lock = lock.ReentrantRedLock('')
        test_lock.acquire()
        test_lock.release()

        self.redlock.assert_called_once_with('', retry_delay=50, retry_times=1)
        self.redlock_acquire.assert_called_once_with()
        self.redlock_release.assert_called_once_with()

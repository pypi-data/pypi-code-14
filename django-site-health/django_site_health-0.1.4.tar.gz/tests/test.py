from unittest.mock import patch

from django.test import TestCase, Client
from django.db import OperationalError

from django_site_health import constants


print('WTF')


class WebTest(TestCase):

    url_path = '/health/'

    def setUp(self):
        super(WebTest, self).setUp()
        self.client = Client()


class DBMockMixin(object):

    def setUp(self):
        super(DBMockMixin, self).setUp()
        self._db_patcher = patch('django_site_health.views.connections')
        mock_connections = self._db_patcher.start()
        self._db_cursor = mock_connections['default'].cursor

    def db_disconnect(self):
        self._db_cursor.side_effect = OperationalError()

    def tearDown(self):
        self._db_patcher.stop()


class FSMockMixin(object):

    def setUp(self):
        super(FSMockMixin, self).setUp()
        self._fs_patcher = patch('django_site_health.views.NamedTemporaryFile')
        self._fs_tempfile = self._fs_patcher.start()

    def fs_disconnect(self):
        self._fs_tempfile.side_effect = OSError()

    def tearDown(self):
        self._fs_patcher.stop()


class DBDisconnectedTests(DBMockMixin, WebTest):

    def test_db_connected(self):
        r = self.client.get(self.url_path, status=200)
        self.assertTrue(r.json()[constants.DATABASE])

    def test_db_disconnected(self):
        self.db_disconnect()
        r = self.client.get(self.url_path, status=500)
        self.assertFalse(r.json()[constants.DATABASE])

        with self.settings(DJANGO_SITE_HEALTH_FAILURE_CHECKS=(constants.FILESYSTEM,)):
            r = self.client.get(self.url_path, status=200)
            self.assertFalse(r.json()[constants.DATABASE])


class FSTests(FSMockMixin, WebTest):

    def test_fs_writeable(self):
        r = self.client.get(self.url_path, status=200)
        self.assertTrue(r.json()[constants.FILESYSTEM])

    def test_fs_readonly(self):
        self.fs_disconnect()
        r = self.client.get(self.url_path, status=200)
        self.assertFalse(r.json()[constants.FILESYSTEM])

        with self.settings(DJANGO_SITE_HEALTH_FAILURE_CHECKS=(constants.FILESYSTEM,)):
            r = self.client.get(self.url_path, status=500)
            self.assertFalse(r.json()[constants.FILESYSTEM])

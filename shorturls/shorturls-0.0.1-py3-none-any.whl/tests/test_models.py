# -*- coding: utf-8 -*-

from unittest.mock import patch

from django.test.testcases import TestCase

from shorturls.models import Url


class ModelTests(TestCase):

    def test_save(self):
        """
        Tests that saving an Url object causes it to get a code value.
        """
        url_obj = Url(url='http://www.test-save.com/')
        self.assertEquals(url_obj.code, '')
        url_obj.save()
        self.assertNotEquals(url_obj.code, '')

    @patch('shorturls.models.logger')
    def test_log(self, mock_logger):
        """
        Tests that log() logs.
        """
        url_obj = Url.objects.create(url='http://www.python.org/')
        msg = 'logged message'
        url_obj.log(msg)
        check = 'URL:{0} - [{1}]'.format(url_obj.code, msg)
        mock_logger.info.assert_called_with(check)

    def test_short_url(self):
        """
        Test that get_short_url() returns a short url
        """
        url_obj = Url.objects.create(url='http://www.test-short-url.com/')
        check_url = '/u/{0}/'.format(url_obj.code)
        self.assertEquals(url_obj.get_short_url(), check_url)

    def test_absolute_url(self):
        """
        Test that get_absolute_url() returns the source url
        """
        source_url = 'http://www.test-absolute-url.com/'
        url_obj = Url.objects.create(url=source_url)
        self.assertEquals(url_obj.get_absolute_url(), source_url)

# -*- coding: utf-8 -*-

import json
from django.core.urlresolvers import reverse
from django.test.testcases import TestCase
from django.utils.translation import force_text

from shorturls.utils.shortcuts import get_shorturl
from shorturls.models import Url


class RegisterViewTests(TestCase):

    def setUp(cls):
        cls.register_url = reverse('shorturls:register_url')

    def test_register_no_url(self):
        response = self.client.get(self.register_url)
        self.assertEqual(response.status_code, 400)

    def test_register_url_get(self):
        source_url = 'http://www.google.com/?q=shorturls'
        get_url = "{0}?url={1}".format(self.register_url, source_url)
        short_url = get_shorturl(source_url)
        response = self.client.get(get_url)
        self.assertContains(response, short_url, status_code=200)

    def test_register_url_ajax(self):
        """
        Test that making an AJAX request returns JSON.
        """
        source_url = 'http://www.google.com/?q=shorturls'
        get_url = "{0}?url={1}".format(self.register_url, source_url)
        short_url = get_shorturl(source_url)
        response = self.client.get(get_url,
                                   HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertContains(response, json.dumps({'url': short_url}),
                            status_code=200)

    def test_register_url_post(self):
        source_url = 'http://www.google.com/?q=shorturls'
        short_url = get_shorturl(source_url)
        response = self.client.post(self.register_url, data={
            'url': source_url
        })
        self.assertContains(response, short_url, status_code=200)


class RedirectViewTests(TestCase):

    def test_redirect_short_url(self):
        source_url = 'http://www.google.com/?q=shorturls'
        url_obj, _created = Url.objects.get_or_create(url=source_url)
        redirect_url = reverse('shorturls:redirect_url', kwargs={'code': url_obj.code})  # noqa
        response = self.client.get(redirect_url, follow=True)
        location, status_code = response.redirect_chain[-1]
        self.assertEqual(location, source_url)
        self.assertEqual(status_code, 302)


class MetricsViewTests(TestCase):

    def test_metrics_view(self):
        source_url = 'http://www.google.com/?q=shorturls'
        url_obj, _created = Url.objects.get_or_create(url=source_url)
        for n in range(0, 10):
            url_obj.log()
        metrics_url = reverse(
            'shorturls:shorturl_metrics', kwargs={'code': url_obj.code})
        response = self.client.get(metrics_url)
        self.assertContains(response, 'counter', status_code=200)

    def test_metrics_ajax_view(self):
        source_url = 'http://www.google.com/?q=shorturls'
        url_obj, _created = Url.objects.get_or_create(url=source_url)
        metrics_url = reverse(
            'shorturls:shorturl_metrics', kwargs={'code': url_obj.code})
        response = self.client.get(metrics_url,
                                   HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        data = json.loads(force_text(response.content))
        counter_start = data.get("counter", 0)
        for n in range(0, 10):
            url_obj.log()

        response = self.client.get(metrics_url + '?a=1',
                                   HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        data = json.loads(force_text(response.content))
        counter_end = data.get("counter", 0)
        self.assertTrue(counter_end - counter_start == 10)

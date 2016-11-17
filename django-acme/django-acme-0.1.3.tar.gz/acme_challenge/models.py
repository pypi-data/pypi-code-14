# -*- coding: utf-8
from __future__ import unicode_literals, absolute_import

from django.test import TestCase
from django.test import override_settings


@override_settings(
    ACME_CHALLENGE_URL_SLUG="test",
    ACME_CHALLENGE_TEMPLATE_CONTENT="test content"
)
class ACMEViewTest(TestCase):

    def test_view_ok(self):
        """Should render the expected content when slug matches"""
        response = self.client.get("/.well-known/acme-challenge/test")
        self.assertEqual(response.content, b"test content")

    def test_view_not_found(self):
        """Should return a 404 when the slug doesn't match"""
        response = self.client.get("/.well-known/acme-challenge/test2")
        self.assertEqual(response.status_code, 404)

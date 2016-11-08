from django.conf import settings
from django.test import TestCase

try:
    from django.urls import reverse
except ImportError:
    from django.core.urlresolvers import reverse


class TestMiddleware(TestCase):
    def test_no_middleware_false_positive(self):
        response = self.client.get(reverse('index'))
        self.assertContains(response, 'hello')
        self.assertFalse(response.has_header('X-Frame-Options'))

    def test_middleware_after_ours_still_works(self):
        new_middleware = list(settings._MIDDLEWARE) + ['django.middleware.clickjacking.XFrameOptionsMiddleware']
        if settings.NO_NEW_STYLE_MIDDLEWARE:
            new_settings = {'MIDDLEWARE_CLASSES': new_middleware}
        else:
            new_settings = {'MIDDLEWARE': new_middleware}

        with self.settings(**new_settings):
            response = self.client.get(reverse('index'))
            self.assertContains(response, 'hello')
            self.assertTrue(response.has_header('X-Frame-Options'))

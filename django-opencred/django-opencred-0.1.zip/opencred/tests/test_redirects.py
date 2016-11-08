from django.contrib.auth.models import Group, User

from django.test import TestCase

try:
    from django.urls import reverse
except ImportError:
    from django.core.urlresolvers import reverse

from opencred.settings import SETTINGS


class TestRedirects(TestCase):
    PASSWORD = 'password'

    def setUp(self):
        self.group = Group.objects.create(name=SETTINGS.OPENCRED_RESTRICTED_GROUP)

        self.ok_user = User.objects.create_user('ok_user', 'hello@world.com', self.PASSWORD)

        self.bad_user = User.objects.create_user('bad_user', 'goodbye@world.com', self.PASSWORD)
        self.bad_user.groups.add(self.group)

    def _login(self, user):
        self.client.login(username=user.username, password=self.PASSWORD)

    def test_unauthenticated_not_redirected(self):
        response = self.client.get(reverse('index'))
        self.assertContains(response, 'hello')

    def test_ok_user_not_redirected(self):
        self._login(self.ok_user)

        response = self.client.get(reverse('index'))
        self.assertContains(response, 'hello')

    def test_exempt_url_not_redirected(self):
        with self.settings(OPENCRED_EXEMPT_URLS=['.*']):
            self._login(self.bad_user)

            response = self.client.get(reverse('index'))
            self.assertContains(response, 'hello')

    def test_bad_user_redirected(self):
        self._login(self.bad_user)

        response = self.client.get('', follow=True)
        self.assertRedirects(response, self._password_change_url + '?next=/')
        self.assertContains(response, SETTINGS.OPENCRED_RESTRICT_MESSAGE)

    def test_custom_message(self):
        with self.settings(OPENCRED_RESTRICT_MESSAGE='hmmm'):
            self._login(self.bad_user)

            response = self.client.get('', follow=True)
            self.assertRedirects(response, self._password_change_url + '?next=/')
            self.assertContains(response, 'hmmm')

    def test_disable(self):
        with self.settings(OPENCRED_DISABLE_RESTRICTIONS=True):
            self._login(self.bad_user)

            response = self.client.get(reverse('index'))
            self.assertContains(response, 'hello')

    @property
    def _password_change_url(self):
        if SETTINGS.OPENCRED_AUTH_BACKEND == 'django-user-accounts':
            return reverse('account_password')
        if SETTINGS.OPENCRED_AUTH_BACKEND == 'contrib-auth':
            return reverse('password_change')
        if SETTINGS.OPENCRED_AUTH_BACKEND == 'allauth':
            return reverse('account_change_password')
        raise ValueError('unkonwn backend %s' % SETTINGS.OPENCRED_AUTH_BACKEND)

from django.contrib.auth.models import Group
from django.contrib.auth.models import User
from django.test import TestCase

try:
    from django.urls import reverse
except ImportError:
    from django.core.urlresolvers import reverse

from opencred.settings import SETTINGS


class TestSignals(TestCase):
    def setUp(self):
        self.group = Group.objects.create(name=SETTINGS.OPENCRED_RESTRICTED_GROUP)

        self.ok_user = User.objects.create_user('ok_user', 'hello@world.com', 'asd')

        self.bad_user = User.objects.create_user('bad_user', 'goodbye@world.com', 'asd')
        self.bad_user.groups.add(self.group)

    def _change_password(self, user, password):
        user.set_password(password)
        user.save()
        if SETTINGS.OPENCRED_AUTH_BACKEND == 'django-user-accounts':
            from account.signals import password_changed
            password_changed.send(self, user=user)
        elif SETTINGS.OPENCRED_AUTH_BACKEND == 'allauth':
            from allauth.account.signals import password_changed
            password_changed.send(self, user=user)
        elif SETTINGS.OPENCRED_AUTH_BACKEND == 'contrib-auth':
            pass

    def test_no_false_positive(self):
        self.assertIn(self.group, self.bad_user.groups.all())

    def test_restrictions_removed_on_password_change(self):
        self._change_password(self.bad_user, 'hello world')

        self.assertNotIn(self.group, self.bad_user.groups.all())

        self._change_password(self.bad_user, 'another password')

        self.assertNotIn(self.group, self.bad_user.groups.all())

    def test_restrictions_not_removed_on_other_change(self):
        self.bad_user.username = 'hello'
        self.bad_user.save()

        self.assertIn(self.group, self.bad_user.groups.all())

        self.bad_user.first_name = 'hello'
        self.bad_user.email = 'hello@jaklsd.com'
        self.bad_user.is_staff = True
        self.bad_user.save()

        self.assertIn(self.group, self.bad_user.groups.all())

    def test_nothing_breaks_on_normal_users(self):
        self._change_password(self.ok_user, 'hello world')

        self.assertNotIn(self.group, self.ok_user.groups.all())

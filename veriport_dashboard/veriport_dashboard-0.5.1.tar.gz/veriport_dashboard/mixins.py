from django.contrib.auth.mixins import UserPassesTestMixin

from .constants import COMPANY


class AdminAccessMixin(UserPassesTestMixin):
    """
    custom mixin to check of admin user access
    """

    def test_func(self):
        return self.request.user.is_superuser


class DashboardAccessMixin(UserPassesTestMixin):
    """
    custom mixin to check of admin user access
    """

    def test_func(self):
        return self.request.user.is_authenticated() and \
            (self.request.user.is_tpa or self.request.user.is_mro or \
            self.request.user.is_employer or self.request.user.is_company or \
            self.request.user.is_superuser)

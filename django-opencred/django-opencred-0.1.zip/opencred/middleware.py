import logging
import re

from django.contrib import messages
from django.contrib.auth.views import redirect_to_login
from django.core.exceptions import MiddlewareNotUsed
from django.utils.translation import ugettext as _

from opencred.settings import SETTINGS

try:
    from django.urls import NoReverseMatch
    from django.urls import reverse
except ImportError:
    from django.core.urlresolvers import NoReverseMatch
    from django.core.urlresolvers import reverse

try:
    from django.utils.deprecation import MiddlewareMixin
except ImportError:
    MiddlewareMixin = object

logger = logging.getLogger(__name__)


class OpenCredMiddleware(MiddlewareMixin):
    def __init__(self, *args, **kwargs):
        if SETTINGS.OPENCRED_DISABLE_RESTRICTIONS:
            raise MiddlewareNotUsed('OPENCRED_DISABLE_RESTRICTIONS is True')

        self._password_change_url = self._get_password_change_url()
        self._exempt_url_regex_list = []
        self._build_exempt_urls()
        super(OpenCredMiddleware, self).__init__(*args, **kwargs)

    def _get_password_change_url(self):
        if SETTINGS.OPENCRED_AUTH_BACKEND == 'contrib-auth':
            return reverse('password_change')
        if SETTINGS.OPENCRED_AUTH_BACKEND == 'django-user-accounts':
            return reverse('account_password')
        if SETTINGS.OPENCRED_AUTH_BACKEND == 'allauth':
            return reverse('account_change_password')

    def _build_exempt_urls(self):
        # django admin panel
        self._add_exempt_url_name('admin:index', prefix=True)

        # django.contrib.auth
        self._add_exempt_url_name('logout'),
        self._add_exempt_url_name('password_change'),
        self._add_exempt_url_name('password_change_done'),
        self._add_exempt_url_name('password_reset'),
        self._add_exempt_url_name('password_reset_done'),
        self._add_exempt_url_name('password_reset_confirm'),
        self._add_exempt_url_name('password_reset_complete'),

        # django-user-accounts
        self._add_exempt_url_name('account_logout')
        self._add_exempt_url_name('account_confirm_email')
        self._add_exempt_url_name('account_password')
        self._add_exempt_url_name('account_password_reset')
        self._add_exempt_url_name('account_password_reset_token')

        # allauth
        self._add_exempt_url_name('account_logout'),
        self._add_exempt_url_name('account_change_password'),
        self._add_exempt_url_name('account_set_password'),
        self._add_exempt_url_name('account_reset_password'),
        self._add_exempt_url_name('account_reset_password_done'),
        self._add_exempt_url_name('account_reset_password_from_key'),
        self._add_exempt_url_name('account_reset_password_from_key_done'),

        # user settings
        for url in SETTINGS.OPENCRED_EXEMPT_URLS:
            self._add_exempt_url(url)

    def _add_exempt_url_name(self, name, prefix=False):
        try:
            self._add_exempt_url('^%s%s' % (reverse(name), '' if prefix else '$'))
        except NoReverseMatch:
            pass

    def _add_exempt_url(self, url_regex):
        self._exempt_url_regex_list.append(re.compile(url_regex))

    def _should_redirect_request(self, request):
        for url_regex in self._exempt_url_regex_list:
            if url_regex.match(request.path):
                logger.debug('skipping %s because it matches %s', request.path, url_regex)
                return False

        return True

    def _should_force_password_change(self, request):
        return request.user.groups.filter(name=SETTINGS.OPENCRED_RESTRICTED_GROUP).exists()

    def process_request(self, request):
        if not self._should_redirect_request(request):
            return

        if self._should_force_password_change(request):
            logger.info('user %s must change its password', request.user)

            # TODO if django.contrib.messages.middleware.MessageMiddleware
            messages.error(request, _(SETTINGS.OPENCRED_RESTRICT_MESSAGE))

            # not really a login page, but the function does what we need (add ?next=...)
            return redirect_to_login(request.path, self._password_change_url)

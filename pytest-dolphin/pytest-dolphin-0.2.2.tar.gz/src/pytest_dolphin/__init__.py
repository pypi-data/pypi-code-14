import pytest
from django.core.urlresolvers import reverse


@pytest.fixture()
def django_logout_url(live_server_reverse):
    return live_server_reverse('django.contrib.auth.views.logout')


@pytest.fixture()
def django_login_url(live_server_reverse):
    return live_server_reverse('django.contrib.auth.views.login')


@pytest.fixture(scope='session')
def live_server_reverse(live_server):
    def django_reverse_server_url(url_pattern_name, hostname=None):
        url = live_server.url if hostname is None else live_server.url.replace('localhost', hostname)
        if url_pattern_name.startswith('/'):
            return url + url_pattern_name
        else:
            return url + reverse(url_pattern_name)

    return django_reverse_server_url


@pytest.fixture
def bar(request):
    return request.config.option.dest_foo

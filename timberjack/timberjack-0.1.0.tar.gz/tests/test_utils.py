import pytest

from timberjack import utils
from timberjack.compat import mock


def test_get_username_from_request_with_logged_in_user(rf):
    email = 'king_commerce@test.com'

    user = mock.Mock(username=email,
                     is_authenticated=mock.Mock(return_value=True))
    user.configure_mock(name='authenticated_user')

    request = rf.get('/')
    request.user = user

    assert utils.get_username_from_request(request) == email


def test_get_username_from_request_with_anonymous_user(rf):
    email = 'king_commerce@test.com'

    user = mock.Mock(username=email,
                     is_authenticated=mock.Mock(return_value=False))
    user.configure_mock(name='logged_out_user')

    request = rf.get('/')
    request.user = user

    assert utils.get_username_from_request(request) == 'anonymous'


def test_get_username_from_request_without_user(rf):
    request = rf.get('/')
    assert utils.get_username_from_request(request) == 'anonymous'


def test_get_client_ip_from_forwarded_header():
    ip_address = '123.111.222.333'

    request = mock.Mock()
    request.META = {'HTTP_X_FORWARDED_FOR': ip_address}

    assert utils.get_client_ip(request) == ip_address


@pytest.mark.parametrize('ip_addresses', [
    ('123.111.222.333',),
    ('123.111.222.333', '193.123.254.221')])
def test_get_client_ip_from_remote_address(ip_addresses):
    request = mock.Mock()
    request.META = {'REMOTE_ADDR': ip_addresses[0]}

    assert utils.get_client_ip(request) == ip_addresses[0]

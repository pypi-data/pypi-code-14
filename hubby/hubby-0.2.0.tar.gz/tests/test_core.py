import hubby

import responses

import json
import os
import unittest.mock as mock

def test_loads_auth_token(tempfile):
    test_token = 'sometoken'
    tempfile.write(test_token)
    tempfile.write('\n')
    tempfile.close()
    with mock.patch('hubby.get_token_file', lambda: tempfile.name):
        token_read = hubby.read_token()

    assert token_read == test_token


def test_loads_auth_token_nonexistent():
    with mock.patch('hubby.get_token_file', lambda: 'foobar'):
        token_read = hubby.read_token()

    assert token_read is None


def test_store_token(tempfile):
    tempfile.close()
    os.remove(tempfile.name)
    test_token = 'foobar'
    with mock.patch('hubby.get_token_file', lambda: tempfile.name):
        hubby.store_token(test_token)

    with open(tempfile.name) as fh:
        assert fh.read() == 'foobar\n'


def test_store_token_existing_file(tempfile):
    tempfile.close()
    test_token = 'foobar'
    with mock.patch('hubby.get_token_file', lambda: tempfile.name):
        hubby.store_token(test_token)

    with open(tempfile.name) as fh:
        assert fh.read() == 'foobar\n'


@responses.activate
def test_create_auth_token():
    test_token = 'foobar'
    responses.add(responses.POST, 'https://api.github.com/authorizations',
        json={'token': test_token})

    with mock.patch('hubby.read_username', lambda: 'randomuser'), \
            mock.patch('hubby.read_password', lambda: 'randompassword'), \
            mock.patch('hubby.getpass.getuser', lambda: 'localuser'), \
            mock.patch('hubby.get_hostname', lambda: 'somehostname'):
        created_token, session = hubby.create_auth_token()

    assert len(responses.calls) == 1
    assert created_token == test_token
    assert session.headers['authorization'] == 'token foobar'
    request = responses.calls[0].request
    request_body = json.loads(request.body.decode('utf-8'))
    assert request_body['note'] == 'hubby for localuser@somehostname'


@responses.activate
def test_create_auth_token_2fa():
    test_token = 'foobar'
    one_time_password = '123456'
    with responses.RequestsMock(assert_all_requests_are_fired=True) as rsps:
        rsps.add(responses.POST, 'https://api.github.com/authorizations',
            status=401, adding_headers={'X-GitHub-OTP': 'token'})
        rsps.add(responses.POST, 'https://api.github.com/authorizations',
            json={'token': test_token})


        with mock.patch('hubby.read_username', lambda: 'randomuser'), \
                mock.patch('hubby.read_password', lambda: 'randompassword'), \
                mock.patch('hubby.read_otp', lambda: one_time_password):
            created_token, _ = hubby.create_auth_token()

        assert len(rsps.calls) == 2
        assert rsps.calls[1].request.headers['x-github-otp'] == one_time_password
        assert created_token == test_token


def test_get_auth_token_stored():
    test_token = 'foobar'
    with mock.patch('hubby.read_token', lambda: test_token):
        token_read, _ = hubby.get_auth_token()

    assert token_read == test_token


def test_get_auth_token_create():
    test_token = 'foobar'
    with mock.patch('hubby.read_token', lambda: None), \
            mock.patch('hubby.create_auth_token', lambda: (test_token, None)), \
            mock.patch('hubby.store_token', mock.Mock()):
        token_read, _ = hubby.get_auth_token()

    assert token_read == test_token

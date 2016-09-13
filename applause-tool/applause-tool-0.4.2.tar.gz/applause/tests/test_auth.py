import unittest2
import mock
import requests_mock

from ..errors import InvalidLogin
from ..auth import ApplauseAuth

from applause import settings


class TestApplauseAuth(unittest2.TestCase):
    """
    Tests for the Applause OAuth handshake.
    """

    def setUp(self):
        self.auth = ApplauseAuth(client_id='dummy_id', client_secret='dummy_secret')

    def test_init_defaults(self):
        """
        Makes sure an ApplauseAuth object is initialized with defaults.
        """
        CLIENT_ID = 'dummy_ID'
        CLIENT_SECRET = 'dummy_secret'

        default_auth = ApplauseAuth(client_id=CLIENT_ID,
                                    client_secret=CLIENT_SECRET)
        self.assertEqual(default_auth.client_id, CLIENT_ID)
        self.assertEqual(default_auth.client_secret, CLIENT_SECRET)
        self.assertEqual(default_auth.oauth_base_url, settings.OAUTH_BASE_URL)

    def test_init_with_custom_url(self):
        """
        Makes sure an ApplauseAuth object accepts extra settings.
        """
        CLIENT_ID = 'dummy_ID'
        CLIENT_SECRET = 'dummy_secret'
        OAUTH_BASE_URL = 'dummy_base_url'

        default_auth = ApplauseAuth(client_id=CLIENT_ID,
                                    client_secret=CLIENT_SECRET,
                                    oauth_base_url=OAUTH_BASE_URL)
        self.assertEqual(default_auth.client_id, CLIENT_ID)
        self.assertEqual(default_auth.client_secret, CLIENT_SECRET)
        self.assertEqual(default_auth.oauth_base_url, OAUTH_BASE_URL)

    def test_create_session(self):
        """
        Makes sure proper client credentials are embedded in the generated
        HTTPS session.
        """
        self.assertEquals(self.auth.session.auth, ('dummy_id', 'dummy_secret'))

    def test_generate_session(self):
        """
        Make sure that proper headers are placed in a generated http session.
        """
        session = ApplauseAuth.generate_requests_session(access_token='dummy')

        self.assertIn('Authorization', session.headers)
        self.assertEquals(session.headers['Authorization'], 'Bearer {token}'.format(token='dummy'))

        self.assertIn('Accept', session.headers)
        self.assertEquals(session.headers['Accept'], 'application/json')

    @mock.patch.object(ApplauseAuth, '_get_access_token')
    def test_login_username_password(self, get_access_token):
        """
        Check the method execution flow for username+password login
        """
        get_access_token.return_value = 'XYZ'

        session = self.auth.login(username='username', password='password')
        get_access_token.assert_called_once_with('username', 'password')
        self.assertEqual("Bearer XYZ", session.headers['Authorization'])
        self.assertEqual("XYZ", self.auth.access_token)

    @mock.patch.object(ApplauseAuth, '_get_access_token')
    def test_login_username_password_empty_token(self, get_access_token):
        """
        Check the method execution flow for username+password login that returns an empty token.
        """
        get_access_token.return_value = ''
        with self.assertRaises(InvalidLogin):
            self.auth.login(username='username', password='password')

        get_access_token.assert_called_once_with('username', 'password')

    def test_login_access_token(self):
        """
        Check the method execution flow for logging in with an existing access token.
        """
        session = self.auth.login(access_token="123")
        self.assertEqual("Bearer 123", session.headers['Authorization'])
        self.assertEqual("123", self.auth.access_token)

    def test_get_access_token_ok(self):
        """
        Check if get_access_token does what it's supposed to do.
        """
        base_url = 'https://www.example.com/oauth/'
        default_auth = ApplauseAuth(client_id=settings.CLIENT_ID,
                                    client_secret=settings.CLIENT_SECRET,
                                    oauth_base_url=base_url)
        url = self.auth.get_oauth_token_url(base_url)
        with requests_mock.Mocker() as m:
            m.post(url, status_code=200, json={'data': {'access_token': 'AT'}})

            access_token = default_auth._get_access_token("username", "password")
            self.assertEqual("AT", access_token)

    def test_get_access_token_response_not_ok(self):
        """
        Check what the behavior of get_access_token is when the response from auth-service is not ok.
        """
        base_url = 'https://www.example.com/oauth/'
        default_auth = ApplauseAuth(client_id=settings.CLIENT_ID,
                                    client_secret=settings.CLIENT_SECRET,
                                    oauth_base_url=base_url)
        url = self.auth.get_oauth_token_url(base_url)
        with requests_mock.Mocker() as m:
            m.post(url, status_code=401, json={'error': 'Invalid credentials!'})

            with self.assertRaises(InvalidLogin):
                default_auth._get_access_token("username", "password")

    def test_get_access_token_no_data(self):
        """
        Check what the behavior of get_access_token is when the response from auth-service is empty.
        """
        base_url = 'https://www.example.com/oauth/'
        default_auth = ApplauseAuth(client_id=settings.CLIENT_ID,
                                    client_secret=settings.CLIENT_SECRET,
                                    oauth_base_url=base_url)
        url = self.auth.get_oauth_token_url(base_url)
        with requests_mock.Mocker() as m:
            m.post(url, status_code=200, json={'some other': 'json content'})

            access_token = default_auth._get_access_token("username", "password")
            self.assertEqual(None, access_token)

    def test_get_access_token_no_token(self):
        """
        Check what the behavior of get_access_token is when the response doesn't contain a token field.
        """
        base_url = 'https://www.example.com/oauth/'
        default_auth = ApplauseAuth(client_id=settings.CLIENT_ID,
                                    client_secret=settings.CLIENT_SECRET,
                                    oauth_base_url=base_url)
        url = self.auth.get_oauth_token_url(base_url)
        with requests_mock.Mocker() as m:
            m.post(url, status_code=200, json={'data': {'still not much': 'access token content'}})

            access_token = default_auth._get_access_token("username", "password")
            self.assertEqual(None, access_token)

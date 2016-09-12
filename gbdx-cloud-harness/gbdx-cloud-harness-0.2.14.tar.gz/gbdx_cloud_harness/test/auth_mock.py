"""
Copied from gbdxtools.
This function returns a mock gbdx-auth requests session with a dummy token.  You can optionally pass in a real token
if you want to actually make requests.
"""

from future import standard_library
standard_library.install_aliases()

from oauthlib.oauth2 import LegacyApplicationClient
from requests_oauthlib import OAuth2Session


def get_mock_gbdx_session(token='dummytoken'):
    s = OAuth2Session(
        client=LegacyApplicationClient('asdf'),
        auto_refresh_url='fdsa',
        auto_refresh_kwargs={
            'client_id':'asdf',
            'client_secret':'fdsa'
        }
    )

    s.token = token
    s.access_token = token
    return s

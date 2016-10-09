# RingPLus Python Wrapper
# See LICENSE for details

"""RingPlus API library"""

__version__ = '0.1.0'
__author__ = 'shatnerz'
__license__ = 'MIT'

from ringplus.models import User, Account
from ringplus.error import RingPlusError, RateLimitError
from ringplus.api import API
from ringplus.auth import OAuthHandler


def debug(enable=True, level=1):
    from six.moves.http_client import HTTPConnection
    HTTPConnection.debuglevel = level

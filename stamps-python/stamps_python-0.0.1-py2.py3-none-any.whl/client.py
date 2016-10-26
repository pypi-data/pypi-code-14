import requests

from requests.exceptions import RequestException

from .authentication import Authentication
from .exceptions import (StampsException, InvalidRequestException,
                         AuthenticationException, ConnectionException)
from .memberships import Memberships
from .redemptions import Redemptions
from .rewards import Rewards
from .transactions import Transactions


AVAILABLE_HOSTS = {
    "ID": "https://stamps.co.id",
    "PH": "https://stamps.ph"
}


class Client(object):

    def __init__(self, token=None, region="ID"):
        # Basic settings
        self.region = region
        self.token = token
        self.base_url = AVAILABLE_HOSTS[region] + "/api"

        # Keep track of the response object for debugging purpose
        self._response = None

        # Attach innerclass
        self.authentication = Authentication(self)
        self.redemptions = Redemptions(self)
        self.transactions = Transactions(self)
        self.memberships = Memberships(self)
        self.rewards = Rewards(self)

    def _call(self, request_type, url, payload):
        try:
            if request_type == 'GET':
                self._response = requests.get(url, params=payload)
            if request_type == 'POST':
                self._response = requests.post(url, json=payload)

        except RequestException as Error:
            raise ConnectionException(None, Error)

        self._handle_api_response(self._response)

        # Return the response as dict for convenience
        return self._response.json()

    def _handle_api_response(self, response):
        # Only OK 200 should return result safely
        if response.status_code == 200:
            return

        exception_to_raise = None
        if response.status_code == 400:
            exception_to_raise = InvalidRequestException
        elif response.status_code == 403:
            exception_to_raise = AuthenticationException
        else:
            exception_to_raise = StampsException

        raise exception_to_raise(response.status_code, response.json(),
                                 response=response)

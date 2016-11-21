import urllib

import requests
from requests import HTTPError

from .local_credentials import read_local_credentials
from .exceptions import SDKError


class ApiConnection(object):
    """
    Takes care of the communication with the ITculate API
    """

    url = "https://api.itculate.io/api/v1"
    # url = "http://localhost:5000/api/v1"

    def __init__(self, api_key=None, api_secret=None, role=None):
        self._session = requests.session()
        self._session.verify = True
        self._session.headers["Content-Type"] = "application/json"
        self._session.headers["Accept"] = "application/json"

        # Apply default role if necessary
        role = role or "admin"

        if api_key is None or api_secret is None:
            # Read permissions from local file (under ~/.itculate/credentials)
            self._session.auth = read_local_credentials(role)

        else:
            self._session.auth = (api_key, api_secret)

        self._last_status_code = 200

    @property
    def last_status_code(self):
        return self._last_status_code

    def get(self, api, expands=None, params=None):
        """
        :param str api: Relative url for api (without parameters)
        :param list[str]|None expands: List of expands to use
        :param dict[str,str]|None params: Any additional query parameters to include
        :return:
        """
        url = "{}/{}".format(self.url, api)

        all_params = dict(params) if params is not None else {}

        if expands:
            # Add the expand section
            all_params["expand"] = ",".join(expands)

        if all_params:
            url += "?{}".format(urllib.urlencode(all_params))

        r = self._session.get(url)
        return self._get_result(r)

    def post(self, api, data=None, json=None, suppress_409=False):
        r = self._session.post("{}/{}".format(self.url, api), data=data, json=json)
        return self._get_result(r, suppress_409=suppress_409)

    def put(self, api, data=None, json=None):
        r = self._session.put("{}/{}".format(self.url, api), data=data, json=json)
        return self._get_result(r)

    def delete(self, api):
        r = self._session.delete("{}/{}".format(self.url, api))
        return self._get_result(r)

    def get_vertices(self, filter=None, limit=100):
        r = self.get("vertices", params={"filter": filter, "limit": limit})
        return []

    def _get_result(self, r, suppress_409=False):
        # Remember the return code
        self._last_status_code = r.status_code
        response_json = r.json()

        try:
            if r.status_code != 409 or suppress_409:
                r.raise_for_status()

            return response_json["result"]

        except HTTPError as e:
            raise SDKError(status_code=r.status_code,
                           error=response_json.get("error"),
                           result=response_json.get("result"),
                           exception=e)

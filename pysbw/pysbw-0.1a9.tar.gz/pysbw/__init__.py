"""
    This is a limited implementation of the Stopbadware data access API.
    This package supports python3 only and is targeted towards private API key users.
"""

import threading
import os
import re
import configparser
import requests
import time
import hashlib
import urllib
from ._version import __version__


class API(object):
    """
        This is a limited implementation of the Stopbadware data access API.

        It is limited in functionality to only retrieve EVENT and IP reports from the API.
        The API does not support search, posting event or looking ASN numbers which are other functionalities that the API
        provides.
    """

    def __init__(self, api_key_file, private_api_key=None, public_api_key=None, max_retries=5,
                 rate_limit={"requests": 40, "seconds": 300}):
        """
        Constructs an API to query the Stopbadware REST API.

        :param api_key_file:  path to key file
        :param private_api_key: alternatively specify private key string instead of using api_key_file
        :param public_api_key: alternatively specify public key string instead of using api_key_file
        :param max_retries: specify this if you want to stop retrying queries after some number of retries. Default is try until you succeed
        :param rate_limit: specify the number of request in period (rate limit) of the API as a dictionary,
                        example: {"requests": 40, "seconds": 300}, that is 40 requests per 300 seconds
        :return: API object
        """

        confpath = os.path.expanduser(api_key_file)

        if not os.path.exists(confpath):
            raise FileExistsError('Could not find API KEY file! Please provide file or provide the api key as input')

        config = configparser.RawConfigParser()
        config.read(confpath)

        priv_key = config.get('sbw', 'apikey')
        if not private_api_key is None:
            priv_key = private_api_key

        pub_key = config.get('sbw', 'publickey')
        if not public_api_key is None:
            pub_key = public_api_key

        self.private_api_key = priv_key
        self.public_api_key = pub_key
        self.retries = max_retries
        self.limits = []
        self.limit_lock = threading.Lock()
        self.rate_limit = rate_limit  # Default is 40 per 5 minutes
        # see: https://stopbadware.atlassian.net/wiki/display/apidocs/Rate+Limits

    def _limit_call_handler(self):
        """
        Ensure we don't exceed the N requests a K seconds limit by leveraging a thread lock.
        This limit is specified with the rate_limit option when creating the API object. (see __init__ )
        """
        # acquire a lock on our threading.Lock() object
        with self.limit_lock:
            # if we have no configured limit, exit.  the lock releases based on scope
            if self.rate_limit['requests'] <= 0:
                return

            now = time.time()
            # self.limits is a list of query times + self.rate_limit['seconds'] seconds.
            # In essence it is a list of times that queries time out of the self.rate_limit['seconds']
            # second query window.

            # this check expires any limits that have passed
            self.limits = [l for l in self.limits if l > now]
            # and we tack on the current query
            self.limits.append(now + self.rate_limit['seconds'])

            # if we have more than our limit of queries (and remember, we call this before we actually
            # execute a query) we sleep until the oldest query on the list (element 0 because we append
            # new queries) times out.  We don't worry about cleanup because next time this routine runs
            # it will clean itself up.
            if len(self.limits) > self.rate_limit['requests']:
                wait_until = self.limits.pop(0)
                time.sleep(wait_until - now)

    def _whatis(self, thing):
        """
        Categorizes the thing it gets passed into one of the items Stopbadware supports
        Returns a sting representation of the type of parameter passed in.

        :param thing: a parameter to identify. this can be a list of things or a thing
        :return: a string representing the identified type of the input thing. If the input thing is a list the
         first element of the list is used to identify.
        """
        # per the API, bulk requests must be of the same type
        # ignore that you can intersperse scan IDs and hashes for now
        # ...although, does that actually matter given the API semantics?
        if isinstance(thing, list):
            thing = thing[0]

        if isinstance(thing, int):
            return "%s" % API_Constants.TIMESTAMP

        # implied failure case, thing is neither a list or an timestamp, so we assume string
        if not isinstance(thing, str):
            return "%s" % API_Constants.UNKNOWN

        if API_Constants.IP_RE.match(thing):
            return API_Constants.IP
        elif API_Constants.UID_RE.match(thing):
            return API_Constants.UID
        else:
            return API_Constants.UNKNOWN

    def _construct_auth_headers(self, query, headers):
        if "SBW-Key" not in headers:
            headers["SBW-Key"] = self.public_api_key

        # Always refresh timestamp header
        epoch_time = int(time.time())  # unix style timestamp
        headers["SBW-Timestamp"] = str(epoch_time)

        # Always reconstruct signature header
        m = hashlib.sha256()
        m.update(headers["SBW-Key"].encode())
        m.update(headers["SBW-Timestamp"].encode())
        path = urllib.parse.urlparse(query).path
        m.update(path.encode())
        m.update(self.private_api_key.encode())
        headers["SBW-Signature"] = m.hexdigest()

        return headers

    def _get_query(self, query, headers={}, parameters={}):
        """
        Submit a GET request to the Stopbadware API

        :param query: The query (see https://stopbadware.atlassian.net/wiki/display/apidocs/Authentication
                     and https://stopbadware.atlassian.net/wiki/display/apidocs/REST+Resources)
        :param headers: parameters of the query, ONLY use for manually crafting parameters
        :return: JSON formatted response from the API
        """

        self._limit_call_handler()
        headers = self._construct_auth_headers(query, headers)
        response = requests.get(query, headers=headers, params=parameters)

        count_retries = 0
        while not response.ok and ((self.retries < 0) or (self.retries > 0 and count_retries < self.retries)):
            status_code = response.status_code

            # 503 = service is too busy, 429 = Too many requests
            if (status_code == 503) or (status_code == 429):
                if status_code == 429:
                    count_retries += 1
                    time.sleep(120)

                self._limit_call_handler()
                headers = self._construct_auth_headers(query, headers)
                response = requests.get(query, headers=headers, params=parameters)
                continue
            else:
                msg = "Generic API Error: Got HTTP Response Code %d. " % response.status_code
                msg += "This is most probably due to API authentication failure or a bad request."
                raise Exception(msg)

        if not response.ok:  # Tried too many times but failed
            msg = "Generic API Error: Got HTTP Response Code %d. " % response.status_code
            msg += "Tried too many times to recover from this but exceeded retries!"
            raise Exception(msg)

        # HTTP Response is OK
        r_in_json = response.json()
        api_response_code = r_in_json['code']

        # Check if API worked correctly
        if api_response_code == API_Constants.API_CODE_OK:
            return r_in_json
        else:
            error_msg = r_in_json['error']
            msg = "API Error of type %d : %s" % (api_response_code, error_msg)
            raise Exception(msg)

    def retrieve(self, thing, thing_type=None):
        """
        Retrieve data from Stopbadware API based on timestamp or IP

        :param thing: a timestamp or IP address in DOT notation,
        :param thing_type: Optional, a hint to the function as to what you are sending it
        :return: Returns a a dictionary with thing as key and the API json response as the value
                If thing was a list of things to query the results will be a dictionary with every thing in the list
                as a key
        :raises TypeError: if it gets something other than a timestamp or IP
        :raises TypeError: if the Stopbadware API returns something we can't parse.
        """
        # trust the user-supplied type over the automatic identification
        thing_id = self._whatis(thing)
        if thing_type is None:
            thing_type = thing_id

        # Query API for Events since timestamp
        if thing_type == API_Constants.TIMESTAMP or thing_type == API_Constants.UID:
            query = API_Constants.CONST_API_URL + API_Constants.API_ACTION_GET_EVENT_REPORT_SINCE

            if not isinstance(thing, list):
                thing = [thing]

            results = {}
            for ts in thing:
                query_parameters = str(ts)
                try:
                    response = self._get_query(query + query_parameters)
                except:
                    raise TypeError
                results[ts] = response

            result = results
        # Query API for IP(s)
        elif thing_type == API_Constants.IP:

            query = API_Constants.CONST_API_URL + API_Constants.API_ACTION_GET_EVENT_REPORT_IP

            if not isinstance(thing, list):
                thing = [thing]

            results = {}
            for ip in thing:
                query_parameters = str(ip)
                try:
                    response = self._get_query(query + query_parameters)
                except:
                    raise TypeError
                results[ip] = response

            result = results
        else:
            raise TypeError("Unimplemented '%s'." % thing_type)

        return result

    def search_between(self, from_time, to_time):
        """
        Retrieve reports that are between 'from_time' to 'to_time'
        :param from_time: unix style timestamp in UTC
        :param to_time: unix style timestamp in UTC
        :return: return the API json response as value
        """
        query = API_Constants.CONST_API_URL + API_Constants.API_ACTION_SEARCH_EVENT

        query_parameters = {"after": from_time,
                            "before": to_time}
        try:
            response = self._get_query(query, parameters=query_parameters)
        except:
            raise TypeError
        return response


class API_Constants:
    # Regular expressions used internally to match the type of query sent to the virus total API
    IP_RE = re.compile(r"^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$")
    UID_RE = re.compile(r"^[1234567890abcdef]{24,24}$")

    # Constants used to identify the type of query sent to the virus total API
    IP = "ip"
    TIMESTAMP = "timestamp"
    UID = "uid"
    UNKNOWN = "unknown"

    CONST_API_URL = "https://dsp.stopbadware.org/v2/"
    API_ACTION_GET_EVENT_REPORT_SINCE = "events/since/"
    API_ACTION_GET_EVENT_REPORT_UID = API_ACTION_GET_EVENT_REPORT_SINCE
    API_ACTION_GET_EVENT_REPORT_IP = "events/ips/"
    API_ACTION_SEARCH_EVENT = "search/events"

    API_CODE_OK = 20
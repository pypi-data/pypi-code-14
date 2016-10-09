"""For binding API calls to python functions."""
from __future__ import print_function

import re
import requests
import time
import logging
import datetime

from six.moves.urllib.parse import quote

from ringplus.utils import convert_to_utf8_str
from ringplus.error import RingPlusError, RateLimitError
from ringplus.error import is_rate_limit_error_message
from ringplus.models import Model

re_path_template = re.compile('{\w+}')

log = logging.getLogger('ringplus.binder')


def bind_api(**config):
    """Given a configuration, returns a function which makes an API call.

    Args:
        api (API): Instance of an API class.
        path: The path of the api call, ie. '/users/{user_id}/accounts'
        payload_type (str): String defining the payload to be returned.
            default:None
        payload_list (bool): Whether to return a list or not. default:None
        allowed_param (list): List of the allowed parameter strings.
            default: []
        method (str): The request method to be used. default: 'GET'
        post_container (str): The name of the container to be used when
            using 'POST' or 'PUT' methods. default:None
        use_cache (bool): Where to use cache or not. default:False

    """

    class APIMethod(object):

        api = config['api']
        path = config['path']
        payload_type = config.get('payload_type', None)
        payload_list = config.get('payload_list', False)
        allowed_param = config.get('allowed_param', [])
        method = config.get('method', 'GET')
        # post_container is for the weird format used by ring plus for
        # put and post requests, ie params{'account[name']: "John Smith"}
        post_container = config.get('post_container', None)
        use_cache = config.get('use_cache', True)
        session = requests.Session()

        def __init__(self, args, kwargs):
            api = self.api

            self.post_data = kwargs.pop('post_data', None)
            self.retry_count = kwargs.pop('retry_count', api.retry_count)

            self.retry_delay = kwargs.pop('retry_delay', api.retry_delay)
            self.retry_errors = kwargs.pop('retry_errors', api.retry_errors)
            self.wait_on_rate_limit = kwargs.pop('wait_on_rate_limit',
                                                 api.wait_on_rate_limit)
            self.wait_on_rate_limit_notify = kwargs.pop(
                'wait_on_rate_limit_notify', api.wait_on_rate_limit_notify)

            self.parser = kwargs.pop('parser', api.parser)
            self.session.headers = kwargs.pop('headers', {})
            self.build_parameters(args, kwargs)

            # Perform any path variable substitution
            self.build_path()

            self.host = api.host

            # Manually set Host header
            self.session.headers['Host'] = self.host
            # Set version header
            self.session.headers['Accept'] = 'application/vnd.ringplus.v{}'.\
                format(self.api.version)
            # Monitoring rate limits
            self._remaining_calls = None
            self._reset_time = None

        def build_parameters(self, args, kwargs):
            """Configure the parameters to be sent with the request."""
            self.session.params = {}

            for idx, arg in enumerate(args):
                if arg is None:
                    continue
                # convert datetimes to iso 8601 strings
                if isinstance(arg, datetime.datetime):
                    arg = arg.isoformat()
                try:
                    utf8str = convert_to_utf8_str(arg)
                    key = self.allowed_param[idx]
                    if self.method in ('PUT', 'POST') and self.post_container:
                        # Convert to ringplus PUT/POST format
                        if key not in ('account_id', 'user_id'):
                            key = self.post_container + '[{}]'.format(key)
                    self.session.params[key] = utf8str
                except IndexError:
                    raise RingPlusError('Too many parameters supplied!')

            for k, arg in kwargs.items():
                if arg is None:
                    continue
                # convert datetimes to iso 8601 strings
                if isinstance(arg, datetime.datetime):
                    arg = arg.isoformat()
                if k in self.session.params:
                    err = 'Multiple values for parameter %s supplied!' % k
                    raise RingPlusError(err)

                utf8str = convert_to_utf8_str(arg)
                if self.method in ('PUT', 'POST') and self.post_container:
                        # Convert to ringplus PUT/POST format
                        if k not in ('account_id', 'user_id'):
                            k = self.post_container + '[{}]'.format(k)
                self.session.params[k] = utf8str

            log.info("PARAMS: %r", self.session.params)

        def build_path(self):
            """Make appropriate substitutions to build path."""
            for variable in re_path_template.findall(self.path):
                name = variable.strip('{}')

                if name == 'account_id' and \
                           'account_id' not in self.session.params and \
                           self.api.auth:
                    value = self.api.auth.get_account_id()
                elif name == 'user_id' and \
                             'user_id' not in self.session.params and \
                             self.api.auth:
                    value = self.api.get_user_id()
                else:
                    try:
                        value = quote(self.session.params[name])
                    except KeyError:
                        raise RingPlusError('No parameter value found for '
                                            'path variable: %s' % name)
                        del self.session.params[name]

                self.path = self.path.replace(variable, value)

        def execute(self):
            """Make the request."""
            self.api.cached_result = False

            # Build the request URL
            url = self.path
            full_url = 'https://' + self.host + url

            # Query the cache if on is available
            # and this request uses a GET method.
            if self.use_cache and self.api.cache and self.method == 'GET':
                cache_result = self.api.cache.get(url)
                # if cache result found and not expired, return it
                if cache_result:
                    # must restore api reference
                    if isinstance(cache_result, list):
                        for result in cache_result:
                            if isinstance(result, Model):
                                result._api = self.api
                    else:
                        if isinstance(cache_result, Model):
                            cache_result._api = self.api
                    self.api.cached_result = True
                    return cache_result

            # Continue attempting request until successful
            # or maximum number of retries is reached.
            retries_performed = 0
            while retries_performed < self.retry_count + 1:
                # handle running out of api calls
                if self.wait_on_rate_limit:
                    if self._reset_time is not None:
                        if self._remaining_calls is not None:
                            if self._remaining_calls < 1:
                                sleeptime = self._reset_time - int(time.time())
                                if sleeptime > 0:
                                    if self.wait_on_rate_limit_notify:
                                        print("Rate limit reached."
                                              "Sleeping for:", sleeptime)
                                    time.sleep(sleeptime + 5)

                # Apply authentication
                if self.api.auth:
                    auth = self.api.auth.apply_auth()

                # # Request compression if configured
                # if self.api.compression:
                #     self.session.headers['Accept-encoding'] = 'gzip'

                # Execute request
                try:
                    resp = self.session.request(self.method,
                                                full_url,
                                                data=self.post_data,
                                                timeout=self.api.timeout,
                                                auth=auth,
                                                proxies=self.api.proxy)
                except Exception as e:
                    raise RingPlusError('Failed to send request: %s' % e)

                rem_calls = resp.headers.get('x-rate-limit-remaining')
                if rem_calls is not None:
                        self._remaining_calls = int(rem_calls)
                elif isinstance(self._remaining_calls, int):
                    self._remaining_calls -= 1
                reset_time = resp.headers.get('x-rate-limit-reset')
                if reset_time is not None:
                    self._reset_time = int(reset_time)
                if self.wait_on_rate_limit and self._remaining_calls == 0 and (
                        # if ran out of calls before waiting switching,
                        # retry last call
                        resp.status_code == 429 or resp.status_code == 420):
                    continue
                retry_delay = self.retry_delay
                # Exit request loop if non-retry error code
                if resp.status_code == 200:
                    break
                elif (resp.status_code == 429 or resp.status_code == 420) and \
                      self.wait_on_rate_limit:
                    if 'retry-after' in resp.headers:
                        retry_delay = float(resp.headers['retry-after'])
                elif self.retry_errors and \
                        resp.status_code not in self.retry_errors:
                    break

                # Sleep before retrying request again
                time.sleep(retry_delay)
                retries_performed += 1

            # If an error was returned, throw an exception
            self.api.last_response = resp
            if resp.status_code and not 200 <= resp.status_code < 300:
                try:
                    error_msg, api_error_code = \
                        self.parser.parse_error(resp.text)
                except Exception:
                    error_msg = "Error response: status code = %s" \
                        % resp.status_code
                    api_error_code = None

                if is_rate_limit_error_message(error_msg):
                    raise RateLimitError(error_msg, resp)
                else:
                    raise RingPlusError(error_msg, resp,
                                        api_code=api_error_code)

            # Parse the response payload
            result = self.parser.parse(self, resp.text)

            # Store result into cache if one is available.
            if self.use_cache and self.api.cache and \
                    self.method == 'GET' and result:
                self.api.cache.store(url, result)

            return result

    def _call(*args, **kwargs):
        method = APIMethod(args, kwargs)
        if kwargs.get('create'):
            return method
        else:
            return method.execute()

    # Set pagination mode
    if 'cursor' in APIMethod.allowed_param:
        _call.pagination_mode = 'cursor'
    elif 'max_id' in APIMethod.allowed_param:
        if 'since_id' in APIMethod.allowed_param:
            _call.pagination_mode = 'id'
    elif 'page' in APIMethod.allowed_param:
        _call.pagination_mode = 'page'

    return _call

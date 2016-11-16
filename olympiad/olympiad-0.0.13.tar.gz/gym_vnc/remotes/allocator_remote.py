import json
import logging
import requests
import six.moves.urllib.parse as urlparse
import time

from gym.utils import reraise

from gym_vnc import error

logger = logging.getLogger(__name__)

AUTH = ('tyytjgq3envte2j9yv2e', '')

class ServerError(Exception):
    def __init__(self, message, status_code=None):
        super(ServerError, self).__init__(message)
        self.message = message
        if status_code is not None:
            self.status_code = status_code


class Allocator(object):
    def __init__(self, runtime, environment=None, n=1, client=None, address=None, base_url='http://allocator.sci.openai-tech.com'):
        if address is None: address = 'public'
        if address not in ['public', 'pod', 'private']:
            raise error.Error('Bad address type specified: {}. Must be public, pod, or private.'.format(address))

        self.n = n
        self.runtime = runtime.id
        self.environment = environment
        self.client = client
        self.address = address
        self._allocated = []

        self._requestor = AllocatorClient(base_url)

    def _address(self, env):
        try:
            return env[self.address]
        except KeyError:
            reraise(suffix='while parsing {}'.format(env))

    def start(self):
        allocation = self._requestor.allocation_create(self.runtime, self.environment, self.client, self.n)
        logger.info('Received allocation %s: %s.', allocation['id'], allocation)
        self._allocated.append(allocation['id'])

        sleep = 1
        while True:
            sleep = min(sleep + 2, 20)
            waiting = [env['name'] for env in allocation['env_n'] if self._address(env)['ip'] is None]
            if len(waiting) == 0:
                break
            logger.info('Waiting on %s pods to get %s IPs; sleeping for %ss: %s', len(waiting), self.address,  sleep, waiting)
            time.sleep(sleep)
            allocation = self._requestor.allocation_get(allocation['id'])

        remotes = []
        for env in allocation['env_n']:
            address = self._address(env)
            remotes.append('{}:{}+{}'.format(address['ip'], address['vnc_port'], address['rewarder_port']))

        if len(remotes) != self.n:
            raise error.Error('Requested {} remotes but only {} were allocated: {}. This usually means that the missing pods died before booting.'.format(self.n, len(remotes), remotes))

        return remotes

    def close(self):
        pass

    def _release(self, allocation_id):
        # TODO: can't be used in destructor?
        self._requestor.allocation_delete(allocation_id)

class AllocatorClient(object):
    def __init__(self, base_url='http://allocator.sci.openai-tech.com'):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({'Content-type': 'application/json'})

    def _parse_server_error_or_raise_for_status(self, resp):
        try:
            j = resp.json()
        except ValueError:
            pass
        else:
            if resp.status_code == 200:
                return j
            elif "message" in j:  # descriptive message from server side
                raise ServerError(message=j["message"], status_code=resp.status_code)
        # The server should technically have returned a JSON error to us, but apparently not.
        resp.raise_for_status()

    def _post_request(self, route, data):
        url = urlparse.urljoin(self.base_url, route)
        logger.info("POST {}\n{}".format(url, json.dumps(data)))
        resp = self.session.post(urlparse.urljoin(self.base_url, route),
                                 data=json.dumps(data), auth=AUTH)
        return self._parse_server_error_or_raise_for_status(resp)

    def _delete_request(self, route):
        url = urlparse.urljoin(self.base_url, route)
        logger.info("DELETE {}".format(url))
        resp = self.session.delete(url, auth=AUTH)
        return self._parse_server_error_or_raise_for_status(resp)

    def _get_request(self, route):
        url = urlparse.urljoin(self.base_url, route)
        logger.info("GET {}".format(url))
        resp = self.session.get(url, auth=AUTH)
        return self._parse_server_error_or_raise_for_status(resp)

    def allocation_create(self, runtime, environment=None, client=None, n=1):
        route = '/v1/allocations'
        data = {'client': client, 'runtime': runtime, 'environment': environment, 'n': n}
        resp = self._post_request(route, data)
        return resp

    def allocation_get(self, id):
        route = '/v1/allocations/{}'.format(id)
        resp = self._get_request(route)
        return resp

    def allocation_delete(self, id):
        route = '/v1/allocations/{}'.format(id)
        resp = self._post_request(route, {})
        return resp

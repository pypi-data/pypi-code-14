#!/usr/bin/env python

from __future__ import unicode_literals
from simplejson.decoder import JSONDecodeError
import config
import light
import logging
import requests
import sensor
import hueobject


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class HueError(Exception):
    pass


class Bridge(object):
    def __init__(self, hostname, username=None, port=80):
        self.hostname = hostname
        self.port = port
        self._username = username
        self.__contruct_api_url()

    @property
    def username(self):
        return self._username

    @username.setter
    def username(self, value):
        self._username = value
        self.__contruct_api_url()

    def __contruct_api_url(self):
        self.API = 'http://{}:{}/api'.format(
            self.hostname,
            self.port
        )
        if self.username:
            self.API += '/{}'.format(self.username)
        logger.info('Update API URL to: {}'.format(self.API))

    def _request(self, url, method='GET', data=None):
        res = requests.request(url=url, method=method, json=data)
        if not res.ok:
            res.raise_for_status()
        try:
            jr = res.json()
            logger.debug('JSON Response: {}'.format(jr))
            api_response = hueobject.HueApiResponse.factory(jr)
            if type(api_response) is hueobject.HueErrorResponse:
                raise HueError(api_response.description)
            return api_response
        except JSONDecodeError:
            logger.error(
                'Failed to decode JSON from response: {}'.format(res.text)
            )

    @staticmethod
    def from_url(url):
        from urlparse import urlparse
        res = urlparse(url)
        return Bridge(hostname=res.hostname, port=res.port)

    @staticmethod
    def discover(guess=True):
        nupnp = Bridge.discover_nupnp()
        upnp = Bridge.discover_upnp()
        bridges = list(set(upnp + nupnp))
        return bridges[0] if guess and len(bridges) > 0 else bridges

    @staticmethod
    def discover_nupnp():
        r = requests.get('https://www.meethue.com/api/nupnp')
        return [Bridge(x['internalipaddress']) for x in r.json()]

    @staticmethod
    def discover_upnp():
        from netdisco.ssdp import scan

        PHILIPS = 'Royal Philips Electronics'
        BRIDGE_MODELS = ['929000226503', 'BSB002']

        hue_bridges = []
        res = scan()

        for h in res:
            logger.info('Check {}'.format(h))
            device_info = h.description.get('device', None)
            if device_info:
                manufacturer = device_info.get('manufacturer', None)
                model = device_info.get('modelNumber', None)
                if manufacturer == PHILIPS and model in BRIDGE_MODELS:
                    url = h.description['URLBase']
                    if url not in hue_bridges:
                        hue_bridges.append(url)
            else:
                logger.error('NO DEVICE INFO')
        return [Bridge.from_url(x) for x in hue_bridges]

    def create_user(self, devicetype='zhue.py#user'):
        url = 'http://{}:{}/api'.format(self.hostname, self.port)
        data = {'devicetype': devicetype}
        return self._request(method='POST', url=url, data=data)

    def delete_user(self, username):
        url = '{}/config/whitelist/{}'.format(self.API, username)
        return self._request(method='DELETE', url=url)

    def get_full_state(self):
        return self._request(method='GET', url=self.API)

    def _property(self, prop_url):
        url = '{}/{}'.format(self.API, prop_url)
        res = self._request(url)
        return res._json

    @property
    def config(self):
        return config.Config(self, self._property('config'))

    @property
    def lights(self):
        l = []
        for i, v in self._property('lights').iteritems():
            l.append(light.Light(self, i, v))
        return l

    @property
    def sensors(self):
        s = []
        for i, v in self._property('sensors').iteritems():
            s.append(sensor.factory(self, i, v))
        return s

    @property
    def temperature_sensors(self):
        return [x for x in self.sensors if isinstance(x, sensor.TemperatureSensor)]

    @property
    def lightlevel_sensors(self):
        return [x for x in self.sensors if isinstance(x, sensor.LightLevelSensor)]

    def light(self, name, exact=False):
        for l in self.lights:
            if exact:
                if l.name == name:
                    return l
            else:
                if l.name.lower().startswith(name.lower()):
                    return l
        raise HueError('No matching light was found')

    def sensor(self, name, exact=False):
        for s in self.sensors:
            if exact:
                if s.name == name:
                    return s
            else:
                if s.name.lower().startswith(name.lower()):
                    return s
        raise HueError('No matching sensor was found')

    # Hue object discovery
    def __find_new(self, hueobjecttype):
        '''
        Starts a search for new Hue objects
        '''
        assert hueobjecttype in ['lights', 'sensors'], \
            'Unsupported object type {}'.format(hueobjecttype)
        url = '{}/{}'.format(self.API, hueobjecttype)
        return self._request(
            method='POST',
            url=url
        )

    def __get_new(self, hueobjecttype):
        '''
        Get a list of newly found Hue object
        '''
        assert hueobjecttype in ['lights', 'sensors'], \
            'Unsupported object type {}'.format(hueobjecttype)
        url = '{}/{}/new'.format(self.API, hueobjecttype)
        return self._request(url=url)

    def find_new_lights(self):
        return self.__find_new('lights')

    def new_lights(self):
        return self.__get_new('lights')

    def find_new_sensors(self):
        return self.__find_new('sensors')

    def new_sensors(self):
        return self.__get_new('sensors')

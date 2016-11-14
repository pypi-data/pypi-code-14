#!/usr/bin/env python

from __future__ import unicode_literals
from simplejson.decoder import JSONDecodeError
import api_response
import config
import device
import light
import logging
import requests
import sensor


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
            response = api_response.HueApiResponse.factory(jr)
            if type(response) is api_response.HueErrorResponse:
                raise HueError(response.description)
            return response
        except JSONDecodeError:
            logger.error(
                'Failed to decode JSON from response: {}'.format(res.text)
            )

    @staticmethod
    def from_url(url, username=None):
        from urlparse import urlparse
        res = urlparse(url)
        return Bridge(hostname=res.hostname, port=res.port, username=username)

    @staticmethod
    def discover(guess=True, username=None):
        nupnp = Bridge.discover_nupnp(username=username)
        upnp = Bridge.discover_upnp(username=username)
        bridges = list(set(upnp + nupnp))
        return bridges[0] if guess and len(bridges) > 0 else bridges

    @staticmethod
    def discover_nupnp(username=None):
        r = requests.get('https://www.meethue.com/api/nupnp')
        return [Bridge(x['internalipaddress'], username) for x in r.json()]

    @staticmethod
    def discover_upnp(username=None):
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
        return [Bridge.from_url(x, username) for x in hue_bridges]

    def create_user(self, devicetype='zhue.py#user'):
        url = 'http://{}:{}/api'.format(self.hostname, self.port)
        data = {'devicetype': devicetype}
        res = self._request(method='POST', url=url, data=data)
        self.username = res._json['username']
        return res

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
        return config.Config(self._property('config'))

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

    def __regroup_sensors(self):
        d = {}
        for s in self.sensors:
            mac_addr = None
            try:
                mac_addr = s.mac_address
            except:
                pass
            if mac_addr in d:
                d[mac_addr].append(s)
            else:
                d[mac_addr] = [s]
        return d

    @property
    def devices(self):
        devs = []
        sensors_grouped = self.__regroup_sensors()
        for d in filter(None, sensors_grouped):
            devs.append(device.HueDevice.factory(sensors_grouped[d]))
        devs += self.lights
        return devs

    def __get_sensors_by_type(self, sensor_type):
        return [x for x in self.sensors if isinstance(x, sensor_type)]

    @property
    def temperature_sensors(self):
        return self.__get_sensors_by_type(sensor.TemperatureSensor)

    @property
    def light_level_sensors(self):
        return self.__get_sensors_by_type(sensor.LightLevelSensor)

    def __get_devices_by_type(self, device_type):
        if device_type == 'sensor':
            return self.sensors
        elif device_type == 'light':
            return self.lights
        else:
            logger.error('Unknown device type')

    def __get_device(self, device_type, name=None, hue_id=None, exact=False):
        assert name or hue_id, 'Name or Hue ID must be provided'
        for d in self.__get_devices_by_type(device_type):
            if name:
                if exact:
                    if d.name == name:
                        return d
                else:
                    if d.name.lower().startswith(name.lower()):
                        return d
            elif str(d.hue_id) == str(hue_id):
                return d
        raise HueError('No matching device was found')

    def light(self, name=None, hue_id=None, exact=False):
        return self.__get_device('light', name, hue_id, exact)

    def sensor(self, name=None, hue_id=None, exact=False):
        return self.__get_device('sensor', name, hue_id, exact)

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

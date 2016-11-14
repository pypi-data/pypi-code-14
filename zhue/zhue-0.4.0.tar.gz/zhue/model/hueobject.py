from __future__ import unicode_literals
from __future__ import print_function
import re


uuid_mac_regex = re.compile(
    r'(([0-9a-f]{2}[:-]){6}([0-9a-f]{2})):(.+)'
)


class HueObject(object):
    def __init__(self, json):
        self._json = json


class HueLLDevice(HueObject):
    def __init__(self, api_endpoint, bridge, hue_id, *args, **kwargs):
        super(HueLLDevice, self).__init__(*args, **kwargs)
        self.hue_id = hue_id
        self._bridge = bridge
        self.api_endpoint = api_endpoint
        self.API = '{}/{}/{}'.format(
            self._bridge.API,
            self.api_endpoint,
            self.hue_id
        )

    # Shortcut function
    def _request(self, *args, **kwargs):
        if 'url' not in kwargs:
            return self._bridge._request(url=self.API, *args, **kwargs)
        return self._bridge._request(*args, **kwargs)

    def _set_state(self, data):
        url = '{}/state'.format(self.API)
        res = self._request(
            method='PUT',
            url=url,
            data=data
        )
        self.update()
        return res

    def update(self):
        '''
        Update our object's data
        '''
        self._json = self._request(
            method='GET',
            url=self.API
        )._json

    @property
    def manufacturer(self):
        return self._json['manufacturername']

    @property
    def model(self):
        return self._json['modelid']

    @property
    def name(self):
        return self._json['name']

    @name.setter
    def name(self, value):
        self._request(
            method='PUT',
            data={'name': value}
        )
        self.update()

    @property
    def version(self):
        return self._json['swversion']

    @property
    def uuid(self):
        return self._json.get('uniqueid', None)

    def __decompose_uuid(self):
        if self.uuid:
            m = re.match(uuid_mac_regex, self.uuid)
            if m:
                return m.group(1), m.group(4)
        return None, None

    @property
    def mac_address(self):
        mac, _ = self.__decompose_uuid()
        return mac

    @property
    def device_id(self):
        _, dev_id = self.__decompose_uuid()
        return dev_id

    @property
    def type(self):
        return self._json['type']

    @property
    def state(self):
        return self._json['state']

    @property
    def config(self):
        return self._json['config']

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return '<{}: {}>'.format(type(self).__name__, self.name)

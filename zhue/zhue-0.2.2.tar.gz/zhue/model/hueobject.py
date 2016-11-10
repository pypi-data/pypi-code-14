from __future__ import unicode_literals
from __future__ import print_function


class HueObject(object):
    def __init__(self, json):
        self._json = json


class HueDevice(HueObject):
    def __init__(self, api_endpoint, bridge, hue_id, *args, **kwargs):
        super(HueDevice, self).__init__(*args, **kwargs)
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
        return self._json['uniqueid']

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

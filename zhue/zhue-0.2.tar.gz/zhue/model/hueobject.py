from __future__ import unicode_literals
from __future__ import print_function


class HueApiResponse(object):
    def __init__(self, json):
        self._json = json

    @staticmethod
    def factory(json):
        if type(json) is list and len(json) > 0:
            if 'error' in json[0]:
                print('ERROR: {}'.format(json[0]['error']))
                return HueErrorResponse(json[0]['error'])
            elif 'success' in json[0]:
                return HueSuccessResponse(json)
        return HueApiResponse(json)


class HueErrorResponse(HueApiResponse):
    @property
    def description(self):
        return self._json['description']

    @property
    def type(self):
        return self._json['type']

    @property
    def address(self):
        return self._json['address']

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return '{}: {}'.format(type(self).__name__, self.description)

class HueSuccessResponse(HueApiResponse):
    pass


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
        res = self._request(
            method='PUT',
            data={'name': value}
        )
        if type(res) is list and len(res) > 0 and 'success' in res[0]:
            self._json['name'] = res[0]['success']['/{}/{}/name'.format(
                self.api_endpoint, self.hue_id
            )]

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

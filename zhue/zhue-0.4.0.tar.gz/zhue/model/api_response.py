from __future__ import unicode_literals
from __future__ import print_function


class HueApiResponse(object):
    def __init__(self, json):
        self._json = json

    @staticmethod
    def factory(json):
        if type(json) is list and len(json) > 0:
            if 'error' in json[0]:
                return HueErrorResponse(json[0]['error'])
            elif 'success' in json[0]:
                return HueSuccessResponse(json[0]['success'])
        return HueApiResponse(json)

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return '{}: {}'.format(type(self).__name__, self._json)


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


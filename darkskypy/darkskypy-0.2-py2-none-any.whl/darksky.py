# -*- coding: utf-8 -*-
"""
This is the core module, recieves the api key, latitude, longitude,
and optional parameters. It builds the request url, makes a HTTP request
to recieves a utf-8-encoded, JSON-formmated object.
"""

import sys
import os
import requests
from attrdict import AttrDict

# Double check the naming convention for module,class,func stuff


class DarkSky(object):
    """
    Requires that an API key has been set somewhere or is provided.
    Also need to include the longitude and latitude for the location.

    Some attributes of DarkSky:
    self.url            - the full request url
    self.raw_response   - raw output from requests.get(...)
    self.json           - json decoded output equivalent to json.loads(...)
    self.forecast       - attrdict object


    """

    base_url = 'https://api.darksky.net/forecast/'

    # TODO
    # Need to add error catching for bad latlng or missing variables
    def __init__(self, location, **kwargs):
        """
        """
        # the api_key should be stored as an os.environment
        # instead of directly in the code
        API_KEY = os.environ.get('DARKSKY_API_KEY')

        self.latitude = location[0]
        self.longitude = location[1]
        self.api_key = API_KEY if API_KEY else kwargs.get('key', None)
    # See, https://darksky.net/dev/docs/forecast
    # for optional request parameters
        self.params = {
            'exclude': kwargs.get('exclude', None),
            'extend': kwargs.get('extend', None),
            'lang': kwargs.get('lang', 'en'),
            'units': kwargs.get('units', 'auto'),
        }
        if self.api_key is None:
            raise KeyError('Missing API Key')

        self.get_forecast(
            self.base_url,
            apikey=self.api_key,
            latitude=self.latitude,
            longitude=self.longitude,
            params=self.params,
        )

    def get_forecast(self, base_url, **kwargs):
        reply = self._connect(base_url, **kwargs)
        self.forecast = AttrDict(reply)

    def _connect(self, base_url, **kwargs):
        """
        This function buids the url and makes an HTTP request. Returns the
        JSON decoded object.

        Raises the standard request exceptions

        Raises Timeout, TooManyRedirects, RequestException.
        Raises KeyError if headers are not present.
        Raises HTTPError if responde code is not 200.
        Raises ValueError if JSON decoding fails

        Darksy.net will raise a 404 error if latitude or longitude are missing
        """

        url = base_url + '{apikey}/{latitude},{longitude}'.format(**kwargs)

        headers = {'Accept-Encoding': 'gzip, deflate'}
        try:
            r = requests.get(url, headers=headers,
                             params=self.params, timeout=60)
            self.url = r.url

        except requests.exceptions.Timeout:
            print('Error: Timeout')
        except requests.exceptions.TooManyRedirects:
            print('Error: TooManyRedirects')
        except requests.exceptions.RequestException as ex:
            print(ex)
            sys.exit(1)

        # Response Headers see https://darksky.net/dev/docs/response
        try:
            self.cache_control = r.headers['Cache-Control']
            self.x_forecast_api_calls = r.headers['X-Forecast-API-Calls']
            self.x_responde_time = r.headers['X-Response-Time']
        except KeyError as kerr:
            print('Warning: Could not get headers.{0}').format(kerr)

        if r.status_code is not 200:
            raise requests.exceptions.HTTPError('Bad response')

        self.raw_response = r.text
        try:
            self.json = r.json()
        except ValueError as jerr:
            raise jerr
        return self.json

# -*- coding: UTF-8 -*-
""" Yelp v3 API see: https://www.yelp.com/developers/documentation/v3/ """

import json

from six.moves import urllib as urllib
from yelp3.errors import ErrorHandler

API_HOST = 'api.yelp.com'

BUSINESS_SEARCH_PATH     = '/v3/businesses/search'
PHONE_SEARCH_PATH        = '/v3/businesses/search/phone'
TRANSACTION_SEARCH_PATH  = '/v3/transactions/{transaction_type}/search'
BUSINESS_PATH            = '/v3/businesses/{id}'
REVIEWS_PATH             = '/v3/businesses/{id}/reviews'
AUTOCOMPLETE_PATH        = '/v3/autocomplete'


class Client(object):

    def __init__(self, access_token, debug=False):
        self.access_token = access_token
        self._error_handler = ErrorHandler()
        self.debug = debug

    def business_search(self, **url_params):
        return self._make_request(
            path = BUSINESS_SEARCH_PATH,
            url_params = dict(**url_params)
        )

    def phone_search(self, **url_params):
        return self._make_request(
            path = PHONE_SEARCH_PATH,
            url_params = dict(**url_params)
        )

    def transaction_search(self, transaction_type, **url_params):
        return self._make_request(
            path = TRANSACTION_SEARCH_PATH.format(
                transaction_type = transaction_type
            ),
            url_params = dict(**url_params)
        )


    def business(self, _id, **url_params):
        return self._make_request(
            path = BUSINESS_PATH.format(
                id = _id
            ),
            url_params = dict(**url_params)
        )

    def review(self, _id, **url_params):
        return self._make_request(
            path = REVIEWS_PATH.format(
                id = _id
            ),
            url_params = dict(**url_params)
        )

    def autocomplete(self, **url_params):
        return self._make_request(
            path = AUTOCOMPLETE_PATH,
            url_params = dict(**url_params)
        )
    
    @staticmethod
    def _filter_dict(old_dict, cb):
        """ Returns a filtered dictionary based on the result of `cb(key)`. """
        return {k: v for k, v in old_dict.items() if cb(k)}
    
    def _make_request(self, path, url_params={}):

        # filter out parameters that equal None
        url_params = Client._filter_dict(url_params, lambda k: url_params[k] is not None)

        url = 'https://{0}{1}?'.format(
            API_HOST,
            urllib.parse.quote(path.encode('utf-8'))
        ) + urllib.parse.urlencode(url_params)

        request = urllib.request.Request(
            url,
            headers = {
                "Authorization": "Bearer {0}".format(self.access_token)
            }
        )

        try:
            conn = urllib.request.urlopen(request)
        except urllib.error.HTTPError as error:
            self._error_handler.raise_error(error)

        try:
            data = conn.read()
            response = json.loads(data.decode('utf-8'))

            if self.debug:
                print("\n> " + request.get_full_url())
                print("")
                print(str(conn.info()))

        finally:
            conn.close()

        return response


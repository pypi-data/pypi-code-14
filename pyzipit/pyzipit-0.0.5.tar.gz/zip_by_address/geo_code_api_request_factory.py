import os
import urllib


class GeoCodeApiRequestFactory:
    def __init__(self, api_key=os.environ['GOOGLE_MAPS_API_KEY']):
        self.api_key = api_key
        self.root = 'https://maps.googleapis.com/maps/api/geocode/json?key={}&'.format(self.api_key)

    def get_address_from_lat_long_request(self, latitude, longitude, language='en'):
        return '{}latlng={},{}&language={}'.format(self.root, latitude, longitude, language)

    def get_lat_long_from_address_request(self, address):
        address_query_form = ','.join(map(urllib.parse.quote, (address.street_number, address.street, address.city,
                                                               address.state, address.country)))
        return '{}address={}'.format(self.root, address_query_form)

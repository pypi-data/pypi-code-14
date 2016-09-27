import io
import json
import os
import urllib.request

from zip_by_address.address import Address


class AddressByCoordinatesResolver:
    _GM__REVERSE_JSON_ADDRESS = 'https://maps.googleapis.com/maps/api/geocode/json?&latlng'

    def __init__(self, language='en', latitude=-1, longitude=-1):
        self.language = language
        self.latitude = latitude
        self.longitude = longitude

    def resolve_address(self):
        request_url = '{}={},{}&key={}&language={}'.format(
            self._GM__REVERSE_JSON_ADDRESS, self.latitude, self.longitude, os.environ['GOOGLE_MAPS_API_KEY'],
            self.language)
        with urllib.request.urlopen(request_url) as response, \
                io.TextIOWrapper(response, encoding=response.headers.get_content_charset('utf-8')) as f:
            results = json.load(f)
        if results['status'] != 'OK':
            raise RuntimeError('Unable to get address from coordinates ({}, {}). Request ended with status {}'.format(
                self.latitude, self.longitude, results['status'])
            )

        desired_info = {address_part: '' for address_part in ('country', 'state', 'city', 'street', 'street_number')}
        for result in results['results']:
            address_components = result['address_components']
            for component in address_components:
                if 'street_number' in component['types'] and desired_info['street_number'] == '':
                    desired_info['street_number'] = int(component['long_name'].split('-')[0])
                elif 'route' in component['types'] and desired_info['street'] == '':
                    desired_info['street'] = component['long_name']
                elif 'locality' in component['types'] and desired_info['city'] == '':
                    desired_info['city'] = component['long_name']
                elif 'administrative_area_level_1' in component['types'] and desired_info['state'] == '':
                    desired_info['state'] = component['long_name']
                elif 'country' in component['types'] and desired_info['country'] == '':
                    desired_info['country'] = component['long_name']
                if all(desired_info.values()):
                    break
        return Address(**desired_info)

import io
import json
import os
import urllib.request

from zip_by_address.address import Address


class CoordinatesByAddressResolver:
    _GM_GEOCODING_API = 'https://maps.googleapis.com/maps/api/geocode/json?address={ADDRESS}&key={KEY}'

    def __init__(self, address=Address()):
        self.address = address

    def resolve_coords(self):
        address_query_form = ','.join(
            map(urllib.parse.quote, (self.address.street_number, self.address.street, self.address.city,
                                     self.address.state, self.address.country)))
        request_url = self._GM_GEOCODING_API.format(ADDRESS=address_query_form, KEY=os.environ['GOOGLE_MAPS_API_KEY'])
        with urllib.request.urlopen(request_url) as response, \
                io.TextIOWrapper(response, encoding=response.headers.get_content_charset('utf-8')) as f:
            results = json.load(f)
        if results['status'] != 'OK':
            raise RuntimeError('Unable to get coordinates from address {}. Request ended with status {}'.format(
                self.address, results['status'])
            )
        lat_long_dict = results['results'][0]['geometry']['location']
        return lat_long_dict['lat'], lat_long_dict['lng']

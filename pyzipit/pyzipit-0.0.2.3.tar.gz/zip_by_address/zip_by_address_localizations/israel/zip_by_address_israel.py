import io
import json
import urllib.parse
import urllib.request

from zip_by_address.exceptions import NoSuchAddress
from zip_by_address.zip_by_address_resolver import ZipByAddressResolver


class ZipByAddressIsrael(ZipByAddressResolver):
    _ZIP_QUERY_ROOT_URL = 'https://www.israelpost.co.il/zip_data1.nsf/SearchZipJSON?OpenAgent&'

    def _validate_address(self):
        address = self._address
        if not (address.city and ((address.street and address.street_number) or address.pob)):
            raise ValueError('Address must specify either the street and street number or the POB')

    def _resolve_zip_from_validated_address(self):
        address = self._address
        req_components = map(urllib.parse.quote, (address.city, address.pob, address.street, address.street_number,
                                                  address.entrance))
        request_url = '{}Location={}&POB={}&Street={}&House={}&Entrance={}'.format(self._ZIP_QUERY_ROOT_URL,
                                                                                   *req_components)
        with urllib.request.urlopen(request_url) as response, \
                io.TextIOWrapper(response, encoding=response.headers.get_content_charset('utf-8')) as f:
            result = json.load(f)
        raw_zip = result.get('zip')
        if raw_zip is None:
            raise NoSuchAddress(address)
        return int(raw_zip)

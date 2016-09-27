import unittest

from zip_by_address.address import Address
from zip_by_address.address_by_coordinates.address_by_coordinates_localizations.israel. \
    address_by_coordinates_resolver_israel import AddressByCoordinatesResolverIsrael
from zip_by_address.address_by_coordinates.address_by_coordinates_resolver_ut import AddressByCoordinatesResolverUt


class AddressByCoordinatesResolverIsraelUt(AddressByCoordinatesResolverUt):
    @classmethod
    def _gen_test_obj_address_ok(cls):
        test_obj = AddressByCoordinatesResolverIsrael()
        test_obj.latitude = 32.776688
        test_obj.longitude = 35.022945
        yield test_obj, Address('ישראל', 'מחוז חיפה', 'חיפה', 'דרך יעקב דורי')
        test_obj.latitude = 32.076509
        test_obj.longitude = 34.799120
        yield test_obj, Address('ישראל', 'מחוז תל אביב', 'תל אביב יפו', 'עמק ברכה', '27')


# Avoid calling super class's tests: http://stackoverflow.com/a/22836015/2016436
del AddressByCoordinatesResolverUt

if __name__ == '__main__':
    unittest.main()

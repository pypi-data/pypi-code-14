import unittest

from zip_by_address.address import Address
from zip_by_address.address_by_coordinates.address_by_coordinates_resolver import AddressByCoordinatesResolver


class AddressByCoordinatesResolverUt(unittest.TestCase):
    def test_resolve_address_ok(self):
        for test_obj, expected_res in self._gen_test_obj_address_ok():
            self.assertEqual(test_obj.resolve_address(), expected_res)

    def test_resolve_address_error(self):
        for test_obj in self._gen_test_obj_address_error():
            self.assertRaises(RuntimeError, test_obj.resolve_address)

    @classmethod
    def _gen_test_obj_address_ok(cls):
        test_obj = AddressByCoordinatesResolver()
        test_obj.latitude = 40.748140
        test_obj.longitude = -73.985933
        yield test_obj, Address('United States', 'New York', 'New York', 'West 33rd Street', '1')
        test_obj.latitude = 40.731676
        test_obj.longitude = -73.989227
        yield test_obj, Address('United States', 'New York', 'New York', 'East 11th Street', '125')
        test_obj.latitude = 40.729507
        test_obj.longitude = -73.968238
        yield test_obj, Address('United States', 'New York', 'New York', 'East River Bikeway')

    @classmethod
    def _gen_test_obj_address_error(cls):
        test_obj = AddressByCoordinatesResolver()
        test_obj.latitude = 0
        test_obj.longitude = 0
        yield test_obj


if __name__ == '__main__':
    unittest.main()

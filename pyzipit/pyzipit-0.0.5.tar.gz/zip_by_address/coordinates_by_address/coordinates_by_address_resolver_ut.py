import unittest

from zip_by_address.address import Address
from zip_by_address.coordinates_by_address.coordinates_by_address_resolver import CoordinatesByAddressResolver


class CoordinatesByAddressResolverUt(unittest.TestCase):
    def test_resolve_coords_ok(self):
        for test_obj, expected_res in self._gen_test_obj_coords_ok():
            self.assertEqual(test_obj.resolve_coords(), expected_res)

    def test_resolve_coords_error(self):
        for test_obj in self._gen_test_obj_coords_error():
            self.assertRaises(RuntimeError, test_obj.resolve_coords)

    @classmethod
    def _gen_test_obj_coords_ok(cls):
        test_obj = CoordinatesByAddressResolver()
        test_obj.address = Address('United States', 'New York', 'New York', 'West 33rd Street', '1')
        yield test_obj, (40.7478448, -73.9852104)
        test_obj.address = Address('United States', 'New York', 'New York', 'East 11th Street', '125')
        yield test_obj, (40.7317694, -73.9891064)
        test_obj.address = Address('United States', 'New York', 'New York', 'East River Bikeway')
        yield test_obj, (40.7098667, -73.9897304)

    @classmethod
    def _gen_test_obj_coords_error(cls):
        test_obj = CoordinatesByAddressResolver()
        yield test_obj


if __name__ == '__main__':
    unittest.main()

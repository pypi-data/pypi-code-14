import unittest

from zip_by_address.address import Address
from zip_by_address.zip_by_address_localizations.israel.zip_by_address_israel import ZipByAddressIsrael
from zip_by_address.zip_by_address_resolver_ut_base import ZipByAddressResolverUtBase


class ZipByAddressIsraelUt(unittest.TestCase, ZipByAddressResolverUtBase):
    def _get_badly_formed_addresses_tests(self):
        ret = [
            Address(city='תל אביב', street='לא קיים'),
            Address(city='תל אביב', street_number=16),
            Address(street='שדרות רוטשילד', street_number=16)
        ]
        return ret

    def _get_no_such_address_tests(self):
        ret = [
            Address(city='תל אביב', street='לא קיים', street_number=16)
        ]
        return ret

    def _get_addresses_to_zip_tests(self):
        ret = {
            Address(city='ירושלים', pob=71117): 9171002,
            Address(city='תל אביב', street='שדרות רוטשילד', street_number=16): 6688119,
        }
        return ret

    def _get_obj_under_test(self, address):
        return ZipByAddressIsrael(address)


if __name__ == '__main__':
    unittest.main()

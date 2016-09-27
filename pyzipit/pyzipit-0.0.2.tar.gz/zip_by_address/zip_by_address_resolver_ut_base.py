from abc import ABCMeta, abstractmethod

from zip_by_address.exceptions import NoSuchAddress


class ZipByAddressResolverUtBase(metaclass=ABCMeta):
    def test_resolve_zip(self):
        addresses_to_zip_tests = self._get_addresses_to_zip_tests()
        for address, expected_zip in addresses_to_zip_tests.items():
            obj_under_test = self._get_obj_under_test(address)
            self.assertEqual(obj_under_test.resolve_zip(), expected_zip)

    def test_no_such_address(self):
        no_such_address_tests = self._get_no_such_address_tests()
        for address in no_such_address_tests:
            obj_under_test = self._get_obj_under_test(address)
            with self.assertRaises(NoSuchAddress):
                obj_under_test.resolve_zip()

    def test_verify_address(self):
        badly_formed_addresses_tests = self._get_badly_formed_addresses_tests()
        for address in badly_formed_addresses_tests:
            with self.assertRaises(ValueError):
                self._get_obj_under_test(address)

    @abstractmethod
    def assertEqual(self, first, second, msg=None):
        pass

    @abstractmethod
    def assertRaises(self, expected_exception, *args, **kwargs):
        pass

    @abstractmethod
    def _get_addresses_to_zip_tests(self):
        pass

    @abstractmethod
    def _get_obj_under_test(self, address):
        pass

    @abstractmethod
    def _get_no_such_address_tests(self):
        """
        :rtype: list
        """

    @abstractmethod
    def _get_badly_formed_addresses_tests(self):
        """
        :rtype: list
        """

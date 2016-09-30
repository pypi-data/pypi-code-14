import unittest

from adaptivepy.component.proxy import Proxy


class SomeClass:
    def __init__(self, val):
        self.__val = val

    def add_to_val(self, amount=None):
        self.__val += amount or 1

    def sub_to_val(self, amount=None):
        self.__val -= amount or 1

    def value(self):
        return self.__val


class SomeInheritedClass(SomeClass):
    def __init__(self, val):
        super().__init__(val + 2)

    def add_to_val(self, amount=None):
        super().add_to_val(amount or 2)

    def compute_mult_val(self, amount):
        return super().value() * amount


class ProxyTestCase(unittest.TestCase):
    def setUp(self):
        self.obj = SomeClass(5)
        self.inherited_obj = SomeInheritedClass(5)

        self.obj_proxy = Proxy(self.obj)
        self.inherited_obj_proxy = Proxy(self.inherited_obj)
        self.empty_proxy = Proxy(None)

    def test_delegate(self):
        self.assertIsNone(self.empty_proxy.delegate())
        self.assertIs(self.obj, self.obj_proxy.delegate())

    def test_update_delegate(self):
        self.empty_proxy.update_delegate(None)
        self.empty_proxy.update_delegate(self.obj)
        self.assertIs(self.obj, self.empty_proxy.delegate())
        self.empty_proxy.update_delegate(None)
        self.assertIsNone(self.empty_proxy.delegate())

        self.obj_proxy.update_delegate(self.inherited_obj)
        self.assertIs(self.obj_proxy.delegate(), self.inherited_obj)

    def test_proxied_methods(self):
        self.assertEqual(self.obj.value(), self.obj_proxy.value())
        self.assertEqual(5, self.obj_proxy.value())
        self.obj_proxy.add_to_val()
        self.assertEqual(6, self.obj_proxy.value())
        self.assertEqual(self.obj.value(), self.obj_proxy.value())
        self.obj.sub_to_val()
        self.assertEqual(5, self.obj_proxy.value())

        expected_mult = (5 + 2) * 2
        self.assertEqual(expected_mult,
                         self.inherited_obj.compute_mult_val(2))
        self.assertEqual(expected_mult,
                         self.inherited_obj_proxy.compute_mult_val(2))

        expected_add = (5 + 2) + 2
        self.inherited_obj_proxy.add_to_val()
        self.assertEqual(expected_add, self.inherited_obj_proxy.value())
        self.assertEqual(expected_add, self.inherited_obj.value())


if __name__ == '__main__':
    unittest.main()

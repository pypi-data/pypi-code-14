import unittest

from ..structures import StringDescriptor, DictDescriptor, ListDescriptor


# To test our descriptors, we need a class whose attributes are the descriptors.

class Foo(object):
    bar = StringDescriptor()
    baz = DictDescriptor()
    qux = ListDescriptor()


class StringDescriptorTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.foo = Foo()

    def test_attribute_sets_and_gets_correctly(self):
        self.foo.bar = 'foo'
        self.assertEquals('foo', self.foo.bar)

    def test_attribute_must_be_string(self):
        for non_string in [1, [1], {1}, {'1': 1}, (1, 1)]:
            with self.assertRaises(TypeError):
                self.foo.bar = non_string

    def test_attributes_across_instances_are_set_correctly(self):
        foo = Foo()
        fu = Foo()
        foo.bar = 'baz'
        fu.bar = 'buz'
        self.assertEquals('baz', foo.bar)
        self.assertEquals('buz', fu.bar)


class DictDescriptorTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.foo = Foo()

    def test_attribute_sets_and_gets_correctly(self):
        self.foo.baz = {'foo': 'foo'}
        self.assertEquals({'foo': 'foo'}, self.foo.baz)

    def test_attribute_must_be_dict(self):
        for non_dict in [1, [1], {1}, '1', (1, 1)]:
            with self.assertRaises(TypeError):
                self.foo.baz = non_dict

    def test_attributes_across_instances_are_set_correctly(self):
        foo = Foo()
        fu = Foo()
        foo.baz = {'bar': 'bar'}
        fu.baz = {'bur': 'bur'}
        self.assertEquals({'bar': 'bar'}, foo.baz)
        self.assertEquals({'bur': 'bur'}, fu.baz)


class ListDescriptorTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.foo = Foo()

    def test_attribute_sets_and_gets_correctly(self):
        self.foo.qux = ['foo']
        self.assertEquals(['foo'], self.foo.qux)

    def test_attribute_must_be_list(self):
        for non_list in [1, {'1': '1'}, {1}, '1', (1, 1)]:
            with self.assertRaises(TypeError):
                self.foo.qux = non_list

    def test_attributes_across_instances_are_set_correctly(self):
        foo = Foo()
        fu = Foo()
        foo.qux = ['bar']
        fu.qux = ['bur']
        self.assertEquals(['bar'], foo.qux)
        self.assertEquals(['bur'], fu.qux)


if __name__ == "__main__":
    test_cases = [StringDescriptor, DictDescriptor, ListDescriptor]

    for test_case in test_cases:
        suite = unittest.TestLoader().loadTestsFromTestCase(test_case)
        unittest.TextTestRunner(verbosity=2).run(suite)
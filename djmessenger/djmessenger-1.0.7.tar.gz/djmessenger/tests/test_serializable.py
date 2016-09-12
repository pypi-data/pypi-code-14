from __future__ import absolute_import
import unittest
import os
from djmessenger.utils.serializable import Serializable


class ChildClass1(Serializable):
    excludes = ['_hidden1']

    def __init__(self):
        self.attr1 = 1
        self.attr2 = '1'
        self.attr3 = True
        self.attr4 = (1, 11, 111)
        self.attr5 = {'key11': 1, 'key12': '12'}
        self.attr6 = 1.1
        self._hidden1 = True


class ChildClass2(ChildClass1):
    excludes = ['_hidden2', '_hidden1']

    def __init__(self):
        super(ChildClass2, self).__init__()
        self.attr4 = (2, 22, 222)
        self.attr5 = {'key21': 2, 'key22': '22'}
        self.attr6 = 2.2
        self._hidden2 = False


class ParentClass(Serializable):
    custom_obj_map = {
        'attr1': [ChildClass1, object],
        'attr2': [ChildClass2, object]
    }
    excludes = ['_ignore']

    def __init__(self):
        self.attr1 = ChildClass1()
        self.attr2 = ChildClass2()
        self.attr3 = 'parent'
        self._ignore = 'should ignore'


class ParentClass2(Serializable):
    custom_obj_map = {
        'attr1': [ParentClass, object],
        'attr2': [ChildClass1, object],
        'attr3': [ChildClass2, list]
    }

    def __init__(self):
        self.attr1 = ParentClass()
        self.attr2 = ChildClass1()
        self.attr3 = [ChildClass2(), ChildClass2()]


class TestSerializer(unittest.TestCase):
    def test_obj_map(self):
        obj = ParentClass2()
        json_string = obj.serialize()
        robj = ParentClass2.deserialize(json_string)
        self.assertTrue(isinstance(robj, ParentClass2), type(robj))
        self.assertEqual(obj.attr1.attr3, robj.attr1.attr3)
        self.assertEqual(type(robj.attr3), list)
        self.assertTrue(isinstance(robj.attr3[0], ChildClass2))
        self.assertTrue(isinstance(robj.attr2, ChildClass1))
        self.assertTrue(obj == robj)

    def test_basic(self):
        obj = ChildClass1()
        json_string = obj.serialize()
        self.assertTrue('_hidden1' not in json_string)
        robj = ChildClass1.deserialize(json_string)
        self.assertTrue('_hidden1' not in dir(robj))
        for key in vars(robj):
            self.assertTrue(key in vars(obj))
        self.assertTrue(obj.attr1, robj.attr1)

    def test_subclass(self):
        obj = ChildClass2()
        json_string = obj.serialize()
        self.assertTrue('_hidden1' not in json_string)
        self.assertTrue('_hidden2' not in json_string)
        robj = ChildClass2.deserialize(json_string)
        self.assertTrue('_hidden1' not in dir(robj))
        self.assertTrue('_hidden2' not in dir(robj))
        for key in vars(robj):
            self.assertTrue(key in vars(obj))
        self.assertTrue(obj.attr1, robj.attr1)

    def test_parent_class(self):
        obj = ParentClass()
        obj1 = obj.attr1
        obj2 = obj.attr2
        json_string_obj1 = obj1.serialize()
        json_string_obj2 = obj2.serialize()
        json_string_parent = obj.serialize()
        self.assertTrue(json_string_obj1 in json_string_parent)

        self.assertTrue(json_string_obj2 in json_string_parent)
        robj = ParentClass.deserialize(json_string_parent)
        self.assertEqual('parent', robj.attr3)

    def test_write_read(self):
        obj = ParentClass()
        file = '/tmp/test_write_read.json'
        obj.write_json(file)
        self.assertTrue(os.path.exists(file))
        robj = ParentClass.read_json(file)
        self.assertEqual('parent', robj.attr3)

    def test_json(self):
        obj = ParentClass()
        jsondict = obj.json()
        self.assertTrue(isinstance(jsondict, dict))
        robj = ParentClass.deserialize(jsondict)
        self.assertEqual(obj.attr3, robj.attr3)

if __name__ == '__main__':
    unittest.main()

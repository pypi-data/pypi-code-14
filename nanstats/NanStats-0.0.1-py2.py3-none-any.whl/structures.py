"""
Descriptors used in the models.py module.

Credit: https://github.com/essence-tech/twitter-ads-api/blob/master/twitter/structures.py
"""
from weakref import WeakKeyDictionary

class BaseDescriptor(object):

    def __init__(self):
        self.data = WeakKeyDictionary()

    def __get__(self, instance, owner):
        return self.data[instance]

 
class StringDescriptor(BaseDescriptor):
    
    def __init__(self):
        super(StringDescriptor, self).__init__()

    def __set__(self, instance, value):
        if value and not isinstance(value, str):
            raise TypeError("{0} is not a string".format(value))
        self.data[instance] = value


class DictDescriptor(BaseDescriptor):

    def __init__(self):
        super(DictDescriptor, self).__init__()

    def __set__(self, instance, value):
        if value and not isinstance(value, dict):
            raise TypeError("{0} is not a dict".format(value))
        self.data[instance] = value


class ListDescriptor(BaseDescriptor):
    
    def __init__(self):
        super(ListDescriptor, self).__init__()

    def __set__(self, instance, value):
        if value and not isinstance(value, list):
            raise TypeError("{0} is not a list".format(value))
        self.data[instance] = value

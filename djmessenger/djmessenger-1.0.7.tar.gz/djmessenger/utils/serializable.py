# Copyright 2016 VMware, Inc.  All rights reserved. -- VMware Confidential
# coding: utf-8
from __future__ import absolute_import

try:
    import simplejson as json
except ImportError:
    import json
import codecs

try:
    # python 2
    basestring
except NameError:
    # python 3
    basestring = str

try:
    # python 2
    unicode
except NameError:
    # python 3
    unicode = str

try:
    xrange
except NameError:
    xrange = range

import logging
from collections import OrderedDict

from .decorators import synchronized
from .filelock import SecureOpen


class Serializable(object):
    """
    Serializable provides an implementation to make an object able to be
    serialized into json as in dict or in string format recursively.

    # Notes

    1. When you subclass another Serializable, think about whether you'd like
       to call superclass's constructor. If you did, you need to take care of
       defining includes and excludes for the attributes defined by superclass

    2. includes and excludes can exist at the same time, but you can't define
       the same attribute in both

    3. Always define custom_obj_map, if nothing should be there, put empty dict.
        Otherwise your class might be inheriting it from superclass and you
        don't it which might lead to unexpected result

    4. Always define includes and excludes, if nothing should be there, put
       them as empty tuple, otherwise your class might be inheriting them from
       superclass and you don't know it which might lead to unexpected result

    # Assumptions

    1. All nested custom objects must implement Serializable
    2. If any attribute is custom object and you need to deserialize it later,
       you need to define it in custom_obj_map so that we know the exactly class
        and if it is contained in either list or dict

    Serializable supports list and dict:

    1. Serialization if the attribute is a list: json() will loop through
       the list and construct another list of dict by calling json() for each
       item
    2. Serialization if the attribute is a dict: json() will loop through
       the dict and construct another dict which key remains exactly the same
       but calling value's json()
    3. Deserialization  of custom objects and custom_obj_map was configured for
       attribute name: deserialize() will first identify the attribute type from
        the loaded json dict. If it was a list of custom objects, we de them one
        by one, put them in a list and assign back to the attribute; if it was
        a dict, construct another dict where key remains the same but de the
        value; if it is an object, just de it

    # Configurations

    ## custom_obj_map

        custom_obj_map provides a way to properly deserialize arbitrary json data into
        this class, since this class itself must know what classes its instance
        variables are, this approach makes sense.
        You only need to put the instance variable whose type is not primitive.
        Follow this format:

        ```
        custom_obj_map = {
            'instance variable name': <class>,
        }
        ```

        This way we know exactly the class of the instance variable and whether it
        is a single object or a list of <class>, either way, deserialzation can
        handle it.

        The <class> can be either a class or a string which matches the class
        name, but the class MUST extends Serializable

    ## excludes

        exclude any attributes that are listed in this tuple.

        includes and excludes can exist at the same time but you can't have the
        same attribute name listed in both

    ## includes

        only include attributes that are listed in this tuple

        includes and excludes can exist at the same time but you can't have the
        same attribute name listed in both

    ## exclude_underscore

        exclude any attributes that starts with an underscore

    ## ordering

        If you want to have certain ordering for the class attributes to display
         in the result of serialize(), you can define this list.

        If `ordering` was not defined, the order is not guaranteed.

        If `ordering` is defined, the output of serialization will be ordered
        by it.

        You are not required to include all attributes in `ordering`, but those
        which are defined in `ordering` will be put before those which are not

    # Quick example:

        ```
        class TestDevice(Serializable):
            def __init__(self, id, type):
                # id and type are both primitive, so no need to use _obj_map
                self.id = id
                self.type = type


        class TestUser(Serializable):
            _obj_map = {
                'devices': ['TestDevice', object]
            }
            excludes = ['password']
            exclude_underscore = True

            def __init__(self, username, password, devices=[], log_location=""):
                super(TestUser, self).__init__(log_location)
                self.username = username
                self.password = password
                self.devices = devices

            def add_device(self, device):
                if isinstance(device, TestDevice):
                    self.devices.append(device)
        ```
    """
    custom_obj_map = {}
    includes = ()
    excludes = ()
    exclude_underscode = True
    ordering = []

    class _Empty(object):
        pass

    def serialize(self, pretty=False):
        """
        Serialize the object into a valid json-formatted string after applying
        includes and excludes policies

        @return: json representation for this instance
        @rtype: str
        """
        d = self.json()
        if pretty:
            return json.dumps(d, sort_keys=True, indent=2)
        else:
            return json.dumps(d, sort_keys=False)

    def json(self):
        """
        Returns an OrderedDict representation of the object, after applying
        includes and excludes policies

        This method takes ordering into account

        @return: a dict represents this object recursively
        @rtype: OrderedDict
        """
        if not self.ordering:
            return self.json_unordered()
        ret = OrderedDict()
        # loop through both ordering and __dict__.keys, which means keys in
        # ordering will be processed first, and dup keys will then be ignored
        for k in self.ordering + self.__dict__.keys():
            # already handled k
            if k in ret:
                continue
            if k in self.includes and k in self.excludes:
                raise AssertionError(
                    'You cannot include attribute %s and exclude it at the same'
                    ' time' % k)
            if self.includes and k not in self.includes:
                continue
            if self.excludes and k in self.excludes:
                continue
            if self.exclude_underscode and k.startswith('_'):
                continue
            # get attribute k from self
            v = getattr(self, k, None)
            # somehow k does not exist???
            if v is None:
                continue
            # if value has attribute json, we use it recursively
            if hasattr(v, "json"):
                ret[k] = v.json()
            elif isinstance(v, list):
                ret[k] = [x.json() if hasattr(x, 'json') else x for x in v]
            elif isinstance(v, dict):
                ret[k] = {k1: (v1.json() if hasattr(v1, 'json') else v1) for k1, v1 in v.items()}
            else:
                ret[k] = v
        return ret

    def json_unordered(self):
        """
        This method does not consider ordering

        @return:
        """
        ret = {}
        for k, v in self.__dict__.items():
            if k in self.includes and k in self.excludes:
                raise AssertionError(
                    'You cannot include attribute %s and exclude it at the same'
                    ' time' % k)
            if self.includes and k not in self.includes:
                continue
            if self.excludes and k in self.excludes:
                continue
            # intentionally leave attribute starts with underscore of
            if self.exclude_underscode and k.startswith('_'):
                continue
            if hasattr(v, "json"):
                ret[k] = v.json()
            elif isinstance(v, list):
                ret[k] = [x.json() if hasattr(x, 'json') else x for x in v]
            elif isinstance(v, dict):
                ret[k] = {k1: (v1.json() if hasattr(v1, 'json') else v1) for k1, v1 in v.items()}
            else:
                ret[k] = v
        return ret

    @classmethod
    def deserialize(cls, json_data):
        """
        Provide default implementation of how to deserialize json representation
         to python object.
        If you have any instance variables that are custom objects and you did
        not define them in custom_obj_map, you need to override deserialize()
        otherwise that instance variable will be deserialized to a dict instead
        of the object itself.

        @param json_data: a dict which represents a json object; or a string
                          which is a valid json format
        @type json_data: dict, str

        @return: an instance of this class
        """
        if not json_data:
            raise ValueError('Not able to deserialize %s from data %s' %
                             (cls.__name__, json_data))
        if isinstance(json_data, str):
            json_data = json.loads(json_data)
        elif isinstance(json_data, dict):
            pass
        else:
            # return json_data
            raise ValueError('json_data only takes either string or dict, but '
                             'was given %s' % type(json_data))
        ret = Serializable._Empty()
        for key in json_data:
            obj_map = cls.custom_obj_map
            if key in obj_map:
                # if key in custom_obj_map, we know it is a custom object
                clazz = obj_map[key][0]
                if isinstance(clazz, str):
                    # the class was defined using class name, search subclasses
                    # of Serializable
                    for subclass in Serializable.__subclasses__():
                        if clazz.upper() == subclass.__name__.upper():
                            clazz = subclass
                            break
                    if isinstance(clazz, str):
                        # not found
                        raise ValueError('Given class %s is a string but that '
                                         'class is not found in Serializable '
                                         'subclasses' % clazz)
                elif isinstance(clazz, type):
                    pass
                ttype = obj_map[key][1]
                if ttype == list:
                    # if it is a list of clazz, we need to de them one by one
                    arr = []
                    for sub in json_data[key]:
                        arr.append(clazz.deserialize(sub))
                    ret.__setattr__(key, arr)
                elif ttype == dict:
                    # if it is a dict
                    d = {}
                    for k, v in json_data[key].items():
                        d[k] = clazz.deserialize(v)
                    ret.__setattr__(key, d)
                else:
                    # it if is a single object, just de it
                    obj = clazz.deserialize(json_data[key])
                    ret.__setattr__(key, obj)
            else:
                # if key is not in custom_obj_map, either it is primitive type
                # or definition not provided, we simply put it as a dict
                ret.__setattr__(key, json_data[key])
        ret.__class__ = cls
        return ret

    @synchronized
    def write_json(self, destination):
        """
        Securely opens the log_location and dumps json from self to it, this
        method is synchronized

        @raise ValueError if log_location was not set
        @raise IOError if log_location can not be opened
        """
        with SecureOpen(destination, codecs.open, False, "w", encoding='utf-8') as fp:
            return json.dump(
                self.json(), fp,
                default=lambda o: {k: v for k, v in o.__dict__.items() if
                                   not k.startswith('_')},
                sort_keys=False,
                indent=2)

    @classmethod
    def read_json(cls, json_file):
        """
        Given an absolute file path, try to decode it as json representation
        to an instance of this class

        @param json_file: absolute file path for the .json file
        @type json_file: str

        @return: an instance of this class
        @raise ValueError: if the json representation can not be deserialized
        @raise IOError: if the file can not be opened
        @raise ValueError: if not able to deserialize the json data into cls
        """
        with open(json_file) as fp:
            json_data = json.load(fp)
            try:
                ret = cls.deserialize(json_data)
            except ValueError as err:
                raise ValueError("The json file provided was not "
                                 "serialized from this class. Underlying error"
                                 "message is %s" % (err.message))
            return ret

    def __eq__(self, other):
        """
        Override __eq__ magic method to compare to Serializables recursively

        @param other:
        @type other: Serializable

        @return: True if the 2 objects are recursively equal; False otherwise
        @rtype: bool
        """
        if not isinstance(other, type(self)):
            return False
        for name, obj in vars(self).items():
            # the following 3 conditions are to honor the include/exclude
            # policy, since either part of the __eq__ method could be an object
            # deserialized from dict or string, the resulting object might not
            # have some attributes
            if self.includes and name not in self.includes:
                continue
            if self.excludes and name in self.excludes:
                continue
            # don't compare attributes startswith underscore
            if self.exclude_underscode and name.startswith('_'):
                continue
            # other does not have this attribute
            if name not in vars(other):
                return False
            # python 2: str and unicode are different classes and deserialized
            # string is unicode, so check with basestring and convert it to
            # unicode for comparison
            if isinstance(obj, basestring):
                obj = unicode(obj)
            other_obj = other.__getattribute__(name)
            if isinstance(other_obj, basestring):
                other_obj = unicode(other_obj)
            # if the attribute was a list before serialization, it will become
            # a tuple after deserialization, so converting both to tuple for
            # comparison
            if isinstance(obj, list):
                obj = tuple(obj)
            if isinstance(other_obj, list):
                other_obj = tuple(other_obj)
            # the attribute types are different
            if not isinstance(other_obj, type(obj)):
                return False
            # only need to check with tuple since we converted all lists to
            # tuples
            if issubclass(obj.__class__, tuple):
                if len(obj) != len(other_obj):
                    return False
                for index in xrange(len(obj)):
                    item = obj[index]
                    other_item = other_obj[index]
                    if hasattr(item, '__eq__') and not item.__eq__(other_item):
                        return False
                    elif not hasattr(item, '__eq__') and item != other_item:
                        return False
            elif issubclass(obj.__class__, dict):
                if len(obj) != len(other_obj):
                    return False
                for key in obj.keys():
                    item = obj[key]
                    other_item = other_obj[key]
                    if hasattr(item, '__eq__') and not item.__eq__(other_item):
                        return False
                    elif not hasattr(item, '__eq__') and item != other_item:
                        return False
            elif hasattr(obj, '__eq__') and not obj.__eq__(other_obj):
                return False
            elif not hasattr(obj, '__eq__') and obj != other_obj:
                return False
        return True


class SerializableEnum(Serializable):
    """
    An Enum-like class, which serializes to a simple string. In json
    serialization, this will be treated just like a string, instead of an
    object

    Usage:

    >>> class Severity(SerializableEnum):
    ...    pass
    >>> Severity.INFO = Severity('INFO', 'INFO')
    >>> Severity.WARNING = Severity('WARNING', 'WARNING')
    >>> Severity.ERROR = Severity('ERROR', 'ERROR')
    >>> Severity.INFO.name == 'INFO'
    True
    >>> Severity.value_of('info') == Severity.INFO
    True
    >>> Severity.value_of('ERROR') == Severity.ERROR
    True
    >>> Severity.value_of('ERROR') == Severity.WARNING
    False
    >>> test = Severity.value_of('TEST')
    Traceback (most recent call last):
    ...
    KeyError: 'name TEST not defined for Severity'
    >>> Severity.INFO.serialize() == 'INFO'
    True
    """
    # _members = set()

    def __init__(self, name, description=""):
        """

        @param name: unique identifier, case sensitive
        @type name: str

        @param description: messages to display
        @type description: str
        """
        self.name = name
        self._description = description
        # self._members.add(self)
        if hasattr(self.__class__, 'members'):
            self.__class__.members[self.name] = self
        else:
            s = dict()
            s[self.name] = self
            setattr(self.__class__, 'members', s)

    def __hash__(self):
        return hash(('%s.%s' % (self.__module__, self.__class__.__name__), self.name))

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        return self.name == other.name

    def serialize(self, pretty=False):
        return self.name

    @classmethod
    def deserialize(cls, json_data):
        """

        @param json_data: this must be a single string
        @return: An instance of Status
        @rtype: Status
        """
        return cls.value_of(json_data)

    def json(self):
        return self.name

    def __repr__(self):
        return '(%s) %s' % (self.__class__.__name__, self.name)

    def __str__(self):
        return self.name

    @classmethod
    def get_members(cls):
        """

        @return: A map maps from enum name to the actual enum instance
        """
        # return {k for k in cls._members if isinstance(k, cls)}
        return getattr(cls, 'members')

    @classmethod
    def value_of(cls, name):
        """
        Given enum name, find and return the corresponding enum object

        @param name: A string for the status code
        @param name: str

        @return: An instance of Status
        @rtype: Status
        @raise KeyError: if name is not defined for the enum
        """
        assert isinstance(name, basestring)
        # for obj in cls.members():
        #     if obj.name == name:
        #         return obj
        if name in cls.get_members():
            return cls.get_members()[name]
        raise KeyError('name %s not defined for %s' % (name, cls.__name__))


if __name__ == '__main__':
    import doctest
    doctest.testmod()

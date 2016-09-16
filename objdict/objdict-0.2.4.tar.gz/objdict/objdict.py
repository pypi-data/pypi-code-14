#
from __future__ import (absolute_import, division,
                        print_function) #, unicode_literals)
import decimal
from collections import namedtuple

try:
    import urllib.parse as urlparselib
except ImportError: #above is python 3
    import urllib as urlparselib
try:
    unicode
except NameError: #no word 'unicode' in python 3
    unicode=str
class DummyClass:
    pass
try:
    from bson.objectid import ObjectId
except ImportError:
    ObjectId=DummyClass

import inspect
import json
#from jsonweb import encode #,decode

import os
import datetime
from collections import OrderedDict

import sys
import types
PY3k = sys.version_info[0] == 3

if PY3k:
    basestring = (str, bytes)
    _iteritems = "items"
else:
    basestring = basestring
    _iteritems = "iteritems"

def items(d):  #this is to become deprecated!
    return getattr(d, _iteritems)()


class ObjDictError(Exception):
    def __init__(self, message, **extras):
        Exception.__init__(self, message)
        self.extras = extras

class ObjectDecodeError(ObjDictError):
    """
    Raised when python containers (dicts and lists) cannot be decoded into
    complex types. These exceptions are raised from within an ObjectHook
    instance.
    """
    def __init__(self, message, **extras):
        ObjDictError.__init__(self, message, **extras)
class ObjectNotFoundError(ObjectDecodeError):
    def __init__(self, obj_type):
        ObjectDecodeError.__init__(
            self,
            "Cannot decode object {0}. No such object.".format(obj_type),
            obj_type=obj_type,
        )

#-----------------------------------------------------------
#  class registry
#-----------------------------------------------------------

class FakeFloat(float):

    def __init__(self, value):
        self._value = value

    def __repr__(self):
        return str(self._value)

from collections import namedtuple #can we used ObjDict instead? circular!
ClsEnc=namedtuple('ClsEnc', 'cls enc')

def type_str(obj):
    return '_'+obj.__class__.__name__ +':' +str(obj)

class ClassRegistry:
    """ The Enc oder table is in two parts.
    exact matches, and 'isinstance' matches.
    classes can have an encoder for the exact class,
    or for any class which matches an isinstance test,
    or separate encoders for both cases

    inst_table is a list of ClsEnc tuples
    exact_table is a dictionary of inst_tables
    """

    def __init__(self):
        self.exact_table={}
        self.inst_table=[]
        self.add_to(decimal.Decimal,FakeFloat)
        self.add_to(datetime.datetime,str)
        self.add_to(datetime.date,str)
        self.add_to(datetime.timedelta,str)
        self.add_to(ObjectId,type_str)

    def add_to(self,cls,encoder,subclasses=False):

        if subclasses:
            lst= inst_table
        else:
            name=cls.__name__
            if not name in self.exact_table:
                self.exact_table[name]=[]
            lst= self.exact_table[name]

        for entry in lst:
            if entry['cls'] == cls:
                entry['enc'] =encoder
                break
        else:
            lst.append(dict(cls=cls,enc=encoder))


    def find(self,cls):
        """ search exact match or isinstance match"""
        lst =  self.exact_table.get(cls.__name__,[])
        for entry in lst:
            if entry['cls'] == cls:
                return entry

        for entry in self.inst_table:
            if isinstance(cls,entry['cls']):
                return entry

        return None

    def do_method(self,entry,obj):
        return entry['enc'](obj)


json_registry = ClassRegistry()
ClassEntry = namedtuple("ClassEntry","cls handler")

class _ClassRegister(object):
    def __init__(self):
        self.__classes = {}
        self.__deferred_updates = {}

    def add_class(self, cls, handler, type_name=None):
        name = type_name or cls.__name__
        self.__classes[name] = ClassEntry(cls,handler)

    def get(self, name):
        """
        Get a handler tuple. Return None if no such handler.
        """
        return self.__handlers.get(name)

    def set(self, name, handler_tuple):
        """
        Add a handler tuple (handler, cls, schema)
        """
        self.__handlers[name] = handler_tuple

    def clear(self):
        self.__handlers = {}
        self.__deferred_updates = {}

    def update_handler(self, name, cls=None, handler=None, schema=None):
        """
        Modify cls, handler and schema for a decorated class.
        """
        handler_tuple = self.__handlers[name]
        self.set(name, self.__merge_tuples((handler, cls, schema),
                                           handler_tuple))

    def xupdate_handler_deferred(self, name, cls=None,
                                handler=None, schema=None):
        """
        If an entry does not exist in __handlers an entry will be added to
        __deferred_updates instead. Then when add_handler is finally called
        values will be updated accordingly. Items in __deferred_updates will
        take precedence over those passed into add_handler.
        """
        if name in self.__handlers:
            self.update_handler(name, cls, handler, schema)
            return
        d = self.__deferred_updates.get(name, (None,)*3)
        self.__deferred_updates[name] = self.__merge_tuples(
            (handler, cls, schema), d)

    def copy(self):
        handler_copy = _ClassRegister()
        [handler_copy.set(n, t) for n, t in self]
        return handler_copy

    def __merge_tuples(self, a_tuple, b_tuple):
        """
        "Merge" two tuples of the same length. a takes precedence over b.
        """
        if len(a_tuple) != len(b_tuple):
            raise ValueError("Iterators differ in length.")
        return tuple([(a or b) for a, b in zip(a_tuple, b_tuple)])

    def __contains__(self, handler_name):
        return handler_name in self.__classes

    def __getitem__(self, handler):
        return self.__classes[handler]

    def __iter__(self):
        for name, handler_tuple in self.__classes.items():
            yield name, handler_tuple

_default_class_register = _ClassRegister()


#------------------------------------------------------------------------
# from json: loading
#------------------------------------------------------------------------

class ObjPairHook(object):
    """
    This class encapsulates the object decode mechanism used to create or
    recreate classes fom json text files.

    An instance of an ObjPairHook provides a decode_pairs() method.
    This method checks for a __type__ specified from the json data.
    If their is no __type__ then the 'BaseHook' object is used to instance
    an object from the Ojbect Pairs. The BaseHook can be a class or any other callable.
    If the BaseHook has a 'from_json' property then this 'from_json' method will
    be called, otherwise the BaseHook will be called directly.

    The 'DefaultType' is actually a default base class for the case where the
    __type__ is specified, but does not correspond to a class in the list of
    classes.
    Pairs hook uses two class lists.  The
    process the data, otherwise Hool does most of the work in managing the handlers that decode the
    json into python class instances. You should not need to use this class
    directly. :func:`make_pairs_hook` is responsible for instantiating and using it.
    """

    def __init__(self, classes_list=[], BaseHook=None,
                BaseType=None):
        #self.classes = classes_list
        self.BaseHook = BaseHook
        self.DefaultType = BaseType
        handle_key = '__from_json__'

        if classes_list:
            _class_register = _default_class_register.copy()
            for cls in classes_list:
                name= cls.__name__
                if name in _class_register:
                    _class_register.update_class(name, **handler_dict)
                else:
                    _class_register.add_class(
                        each_class,
                         getattr(cls,handle_key,cls), name
                        )
        else:
            _class_register = _default_class_register

        self.classes = _class_register


    def from_json(self, obj):
        """
        This method is called for every dict decoded from a json string. The
        presence of the key ``__type__`` in ``obj`` will trigger a lookup in
        ``self.handlers``. If a handler is not found for ``__type__`` then an
        :exc:`ObjectNotFoundError` is raised. If a handler is found it will
        be called with ``obj`` as it only argument. If an :class:`ObjectSchema`
        was supplied for the class, ``obj`` will first be validated then passed
        to handler. The handler should return a new python instant of type ``__type__``.
        """
        if isinstance(obj,list):
            dobj=dict(obj)
            if "__type__" not in dobj:
                if self.BaseHook:
                    return self.BaseHook(obj)
                else:
                    #consider override if no baseHook to ObjDict
                    return dobj
            obj=dobj
        elif "__type__" not in obj:
            if self.BaseHook:
                # do factory with BaseHook entry?
                return self.BaseHook(obj)
            return obj

        obj_type = obj["__type__"]
        try:
            cls, factory = self.classes[obj_type]
        except KeyError:
            if self.DefaultType:
                #print("doing this type")
                #could do:  factory,cls,schema ...?
                ThisType=type(str(obj_type),(self.DefaultType,),
                    {'_set_type':True})
                return ThisType(obj)
            raise ObjectNotFoundError(obj_type)

        try:
            #print("fact ret",cls)
            return factory(obj)
        except KeyError as e:
            raise ObjectAttributeError(obj_type, e.args[0])



#_default_object_handlers = _ObjectHandlers()

def from_json(type_name=None):
    """
    Decorating a class with :func:`from_object` adds
    will allow :func:`json.loads`
    to return instances of that class, embeded within the object returned.

    The class can contain a 'from_json' class method that will receives
    a list of object pairs as a parameter, and return an instance of the class.

    This class method will normally perform any validation on the 'pairs' data
    (key, value list) that is decoded from json and provided as a paramter,
    extract the relevant data and pass that to the class init method.

    If no '__from_json__' class method is present, the the 'pairs' key/value
    list decoded from jsons will be provide as a parmater to the class init method

    Here is an
    example::

        >>> from objdict import ObjDict, from_factoryobject, loader
        >>> @classmethod
        >>> def __from_json__(cls, pairlist):
        ...    obj = ObjDict(pairlist)
        ...    return cls( obj.first_name, obj.last_name )
        ...
        >>> @from_object()
        ... class Person(object):
        ...     def __init__(self, first_name, last_name):
        ...         self.first_name
        ...         self.last_name = last_name
        ...
        >>> person_json = '{"__type__": "Person", "first_name": "Shawn", "last_name": "Adams"}'
        >>> person = loader(person_json)
        >>> person
        <Person object at 0x1007d7550>
        >>> person.first_name
        'Shawn'

    The ``__type__`` key is very important. Without it the 'object_pairs_hook'
    will not simply treat the data as a generic object/dictionary.

    By default
    :func:`ObjPairHook.decode` assumes ``__type__`` will be the class's ``__name__``
    attribute. You can specify your own value by setting the ``type_name``
    keyword argument ::

        @from_object( type_name="PersonObject")

    Which means the json string would need to be modified to look like this::

        '{"__type__": "PersonObject", "first_name": "Shawn", "last_name": "Adams"}'
    """
    handle_key='__from_json__'
    def wrapper(cls):
        _default_class_register.add_class(
            cls, getattr(cls,handle_key,cls), type_name
        )
        return cls
    return wrapper


def make_pairs_hook(classes=None, BaseHook=None, DefaultBase=None):
    """
    Wrapper to generate :class:`ObjectHook`. Calling this function will configure
    an instance of :class:`ObjectHook` and return a callable suitable for
    passing to :func:`json.loads` as ``object_pairs_hook``.

    Dictionaries/objects without a  ``__type__``
    key are encoded as ObjDict objects ::

        >>> json_str = '{"obj":{"inside": "value"}}'
        >>> loader(json_str)
        {"obj":obnj dict
        >>> # lists work too
        >>> json_str = '''[
        ...     {"first_name": "bob", "last_name": "smith"},
        ...     {"first_name": "jane", "last_name": "smith"}
        ... ]'''
        >>> loader(json_str, as_type="Person")
        [<Person object at 0x1007d7550>, <Person object at 0x1007d7434>]

    .. note::

        Assumes every object a ``__type__``  kw is ObjDict

        ``handlers`` is an ObjDict with this format::

        {"Person": {"cls": Person, "handler": person_decoder, "schema": PersonSchema)}

    If you do not wish to decorate your classes with :func:`from_json` you
    can specify the same parameters via the ``classes`` keyword argument.
    Here is an example::

        >>> class Person(object):
        ...    def __init__(self, first_name, last_name):
        ...        self.first_name = first_name
        ...        self.last_name = last_name
        ...
        >>> def person_decoder(cls, obj):
        ...    return cls(obj["first_name"], obj["last_name"])

        >>> handlers = {"Person": {"cls": Person, "handler": person_decoder}}
        >>> person = loader(json_str, handlers=handlers)
        >>> # Or invoking the object_hook interface ourselves
        >>> person = json.loads(json_str, object_pairs_hook=make_pairs_hook(handlers))

    .. note::

        If you decorate a class with :func:`from_json` you can specify
        a list of classes to use
        """

    return ObjPairHook(classes, BaseHook, DefaultBase).from_json


def loader(json_str, **kw):
    """
    Call this function as you would call :func:`json.loads`. It wraps the
    :ref:`make_pairs_hook` interface and returns python class instances from JSON
    strings.

    :param ensure_type: Check that the resulting object is of type
        ``ensure_type``. Raise a ValidationError otherwise.
    :param handlers: is a dict of handlers. see :func:`make_pairs_hook`.
    :param as_type: explicitly specify the type of object the JSON
        represents. see :func:`make_pairs_hook`
    :param validate: Set to False to turn off validation (ie dont run the
        schemas) during this load operation. Defaults to True.
    :param kw: the rest of the kw args will be passed to the underlying
        :func:`json.loads` calls.


    """

    #object_pairs_hook=ObjDict,
    #    DefaultType=DefaultType, parse_float=decimal.Decimal

    baseword="object_pairs_hook"

    #hookword= baseword if baseword in kw else "object_hook"
    kw[baseword] = make_pairs_hook(
        kw.pop("handlers", None),
        kw.pop(baseword, kw.pop("object_hook", ObjDict)),
        kw.pop("DefaultType", ObjDict)
    )

    #ensure_type = kw.pop("ensure_type", _as_type_context.top)

    print("kw dict",kw)

    try:
        obj = json.loads(json_str, **kw)
    except ValueError as e:
        raise JsonDecodeError(e.args[0])

    # if ensure_type:
    #     return EnsureType(ensure_type).validate(obj)
    return obj

##--------------------------------------------------------------------
##--------------------------------------- to json
##--------------------------------------------------------------------


class EncodeArgs:
    __type__ = None
    serialize_as = None
    handler = None
    suppress = None


def std__json__(self,enc=None,internal=False):
    """
    ---note self reference not updated obj is self!

    Handles encoding instance objects of classes decorated by
    :func:`to_object`. Returns a dict containing all the key/value pairs
    in ``obj.__dict__``. Excluding attributes that

    * start with an underscore.
    * were specified with the ``suppress`` keyword argument.

    The returned dict will be encoded into JSON.

    .. note::

        Override this method if you wish to change how ALL objects are
        encoded into JSON objects.

    """
    if not internal:
        return dumps(self)
    encode= self.__json__encode
    suppress = encode.suppress

    if enc and enc._exclude_nulls is not None:
        exclude_nulls = enc._exclude_nulls
    else:
        exclude_nulls = encode.exclude_nulls

    json_obj = {}

    def suppressed(key):
        return key in suppress or (enc and key in enc._hard_suppress)

    for attr in dir(self):
        if not attr.startswith("_") and not suppressed(attr):
            value = getattr(self, attr)
            if value is None and exclude_nulls:
                continue
            if not isinstance(value, types.MethodType):
                json_obj[attr] = value
    if not suppressed("__type__"):
        json_obj["__type__"] = encode.__type__
    return json_obj

def to_json(cls_type=None, suppress=None, handler=None, exclude_nulls=False):
    """
    Decorateor. To make your class instances JSON encodable decorate them with
    :func:`to_object`. The python built-in :py:func:`dir` is called on the
    class instance to retrieve key/value pairs that will make up the JSON
    object (*Minus any attributes that start with an underscore or any
    attributes that were specified via the* ``suppress`` *keyword argument*).

    Here is an example::

        >>> from jsonweb import to_object
        >>> @to_object()
        ... class Person(object):
        ...     def __init__(self, first_name, last_name):
        ...         self.first_name = first_name
        ...         self.last_name = last_name

        >>> person = Person("Shawn", "Adams")
        >>> dumper(person)
        '{"__type__": "Person", "first_name": "Shawn", "last_name": "Adams"}'

    A ``__type__`` key is automatically added to the JSON object. Its value
    should represent the object type being encoded. By default it is set to
    the value of the decorated class's ``__name__`` attribute. You can
    specify your own value with ``cls_type``::

        >>> from jsonweb import to_object
        >>> @to_object(cls_type="PersonObject")
        ... class Person(object):
        ...     def __init__(self, first_name, last_name):
        ...         self.first_name = first_name
        ...         self.last_name = last_name

        >>> person = Person("Shawn", "Adams")
        >>> dumper(person)
        '{"__type__": "PersonObject", "first_name": "Shawn", "last_name": "Adams"}'

    If you would like to leave some attributes out of the resulting JSON
    simply use the ``suppress`` kw argument to pass a list of attribute
    names::

        >>> from jsonweb import to_object
        >>> @to_object(suppress=["last_name"])
        ... class Person(object):
        ...     def __init__(self, first_name, last_name):
        ...         self.first_name = first_name
        ...         self.last_name = last_name

        >>> person = Person("Shawn", "Adams")
        >>> dumper(person)
        '{"__type__": "Person", "first_name": "Shawn"}'

    You can even suppress the ``__type__`` attribute ::

        @to_object(suppress=["last_name", "__type__"])
        ...

    Sometimes it's useful to suppress ``None`` values from your JSON output.
    Setting ``exclude_nulls`` to ``True`` will accomplish this ::

        >>> from jsonweb import to_object
        >>> @to_object(exclude_nulls=True)
        ... class Person(object):
        ...     def __init__(self, first_name, last_name):
        ...         self.first_name = first_name
        ...         self.last_name = last_name

        >>> person = Person("Shawn", None)
        >>> dumper(person)
        '{"__type__": "Person", "first_name": "Shawn"}'

    .. note::

        You can also pass most of these arguments to :func:`dumper`. They
        will take precedence over what you passed to :func:`to_object` and
        only effects that one call.

    If you need greater control over how your object is encoded you can
    specify a ``handler`` callable. It should accept one argument, which is
    the object to encode, and it should return a dict. This would override the
    default object handler :func:`JsonWebEncoder.object_handler`.

    Here is an example::

        >>> from jsonweb import to_object
        >>> def person_encoder(person):
        ...     return {"FirstName": person.first_name,
        ...         "LastName": person.last_name}
        ...
        >>> @to_object(handler=person_encoder)
        ... class Person(object):
        ...     def __init__(self, first_name, last_name):
        ...         self.guid = 12334
        ...         self.first_name = first_name
        ...         self.last_name = last_name

        >>> person = Person("Shawn", "Adams")
        >>> dumper(person)
        '{"FirstName": "Shawn", "LastName": "Adams"}'


    You can also use the alternate decorator syntax to accomplish this. See
    :func:`jsonweb.encode.handler`.

    """
    def wrapper(cls):
        if not hasattr(cls,'__json__'):
            cls.__json__ = std__json__
        encode = EncodeArgs()
        encode.serialize_as = "json_object"
        #cls._encode.handler = handler
        encode.suppress = suppress or []
        encode.exclude_nulls = exclude_nulls
        encode.__type__ = cls_type or cls.__name__
        cls.__json__encode = encode
        return cls #__inspect_for_handler(cls)
    return wrapper



@to_json() #note handled by dict encoder
@from_json()
class ObjDict(OrderedDict):
    #_set_type=False # can be overriden in instance
    def __init__(self,*args,**kwargs):
        set_type= kwargs.pop('_set_type',None)
        self.__keys__= kwargs.pop('__keys__', getattr(self,'__keys__',''))
        if isinstance(self.__keys__,str):
            self.__keys__=self.__keys__.split()
        predata=[]
        if len(args)==1 and isinstance(args[0],str):
            predata=loader(args[0]).items()
            args=[]
        elif self.__keys__ and len(args)== len(self.__keys__):
            predata=zip(self.__keys__,args)
            args=[]
        super(ObjDict,self).__init__(*args,**kwargs)
        if set_type is not None:
            self._set_type=set_type
        for arg in args:
            if isinstance(arg,dict):
                self.__dict__.update(**arg)
        self.__dict__.update(**kwargs)
        #self.update(**args)
        for key,data in predata:
            self[key]=data
    @property
    def _set_type(self):
        return self.__dict__.get(
            '_set_type', self.__class__.__name__ != 'ObjDict')
    @_set_type.setter
    def _set_type(self,value):
        self.__dict__['_set_type'] = value #set inst value hiding property

    def __setitem__(self,key,value):
        super(ObjDict,self).__setitem__(key,value)
        setattr(self,key,value)

    def __setattr__(self,attr,value):
        super(ObjDict,self).__setattr__(attr,value)
        if attr[:1] != '_':
            super(ObjDict,self).__setitem__(attr,value)

    @classmethod
    def __from_json__(cls,thedict):
        """ not really needed in current form """
        print('in handler',cls,thedict)
        return cls(thedict)

    def __str__(self):
        return self.__json__()


class JsonEncoder(json.JSONEncoder):
    """
    This :class:`json.JSONEncoder` subclass is responsible for encoding
    instances of classes that have been decorated with :func:`to_object` or
    :func:`to_list`. Pass :class:`JsonWebEncoder` as the value for the
    ``cls`` keyword argument to :func:`json.dump` or :func:`json.dumps`.

    Example::

        json.dumps(obj_instance, cls=JsonWebEncoder)

    Using :func:`dumper` is a shortcut for the above call to
    :func:`json.dumps` ::

        dumper(obj_instance) #much nicer!

    """

    _DT_FORMAT = "%Y-%m-%dT%H:%M:%S"
    _D_FORMAT = "%Y-%m-%d"

    def __init__(self, **kw):
        self._hard_suppress = kw.pop("suppress", [])
        self._exclude_nulls = kw.pop("exclude_nulls", None)
        self._handlers = kw.pop("handlers", {})
        if not isinstance(self._hard_suppress, list):
            self._hard_suppress = [self._hard_suppress]
        json.JSONEncoder.__init__(self, **kw)

    def default(self, o):
        if hasattr(o,'__json__'):
            e_args = getattr(o,"__json__encode")

            # Passed in handlers take precedence.
            if e_args.__type__ in self._handlers:
                return self._handlers[e_args.__type__](o)
            elif e_args.handler:
                if e_args.handler_is_instance_method:
                    return getattr(o, e_args.handler)()
                return e_args.handler(o)
            elif e_args.serialize_as == "json_object":
                #return self.object_handler(o)
                return o.__json__(self,internal=True)
            elif e_args.serialize_as == "json_list":
                return self.list_handler(o)

        # if isinstance(o, datetime.datetime):
        #     return o.strftime(self._DT_FORMAT)
        # if isinstance(o, datetime.date):
        #     return o.strftime(self._D_FORMAT)

        encoder = json_registry.find(o.__class__)
        if encoder:
            return json_registry.do_method(encoder,o)

        return json.JSONEncoder.default(self, o)



def list_handler(self, obj):
    """
    Handles encoding instance objects of classes decorated by
    :func:`to_list`. Simply calls :class:`list` on ``obj``.

    .. note::

        Override this method if you wish to change how ALL objects are
        encoded into JSON lists.

    """
    return list(obj)

class ObjectEncoderStd(JsonEncoder):
    def encode(self,o):
        if isinstance(o,ObjDict):
            if o._set_type:
                o['__type__'] = o.__class__.__name__
        return super(ObjectEncoderStd,self).encode(o)
    def default(self, o):
        return super(ObjectEncoderStd, self).default(o)

#class ObjectEncoderAll(json.JSONEncoder):
class ObjectEncoderAll(JsonEncoder):
    def default(self, o):
        try:
            return super(ObjectEncoderAll, self).default(o)
        except TypeError as e:
            return str(o)

def dumps(obj, **kw):
    """
    JSON encode your class instances by calling this function as you would
    call :func:`json.dumps`. ``kw`` args will be passed to the underlying
    json.dumps call.

    :param handlers: A dict of type name/handler callable to use.
     ie {"Person:" person_handler}

    :param cls: To override the given encoder. Should be a subclass
     of :class:`JsonWebEncoder`.

    :param suppress: A list of extra fields to suppress (as well as those
     suppressed by the class).

    :param exclude_nulls: Set True to suppress keys with null (None) values
     from the JSON output. Defaults to False.
    """
    return json.dumps(obj, cls=kw.pop("cls", JsonEncoder), **kw)

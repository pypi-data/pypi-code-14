# Quark 1.0.452 run at 2016-10-13 16:26:58.627837
from __future__ import unicode_literals
from __future__ import division
from __future__ import absolute_import
from __future__ import print_function
from builtins import str as unicode

from quark_runtime import *
_lazyImport.plug("quark.reflect")
import quark_runtime
import quark_threaded_runtime
import quark_runtime_logging
import quark_ws4py_fixup
import mdk_runtime_files

class Class(_QObject):
    def _init(self):
        self.id = None
        self.name = None
        self.parameters = _List([])
        self.fields = _List([])
        self.methods = _List([])
        self.parents = _List([])

    def __init__(self, id):
        self._init()
        if ((id) == (u"quark.error.Error")):
            Class.ERROR = self

        (self).id = id
        (Class.classes)[id] = (self);
        (self).name = id

    @staticmethod
    def get(id):
        if ((id) == (None)):
            raise Exception(u"Cannot find class given nil class ID.");

        if (not ((id) in (Class.classes))):
            raise Exception((((u"Cannot find ") + (id)) + (u" in ")) + (_toString(_List(list((Class.classes).keys())))));

        return (Class.classes).get(id)

    def getId(self):
        return self.id

    def getName(self):
        return self.name

    def getParents(self):
        result = _List([]);
        idx = 0;
        while ((idx) < (len(self.parents))):
            (result).append(Class.get((self.parents)[idx]));
            idx = (idx) + (1)

        return result

    def getParameters(self):
        result = _List([]);
        idx = 0;
        while ((idx) < (len(self.parameters))):
            (result).append(Class.get((self.parameters)[idx]));
            idx = (idx) + (1)

        return result

    def isAbstract(self):
        return (self.id) == ((Class.OBJECT).id)

    def construct(self, args):
        return None

    def getFields(self):
        return self.fields

    def getField(self, name):
        idx = 0;
        while ((idx) < (len(self.fields))):
            if ((((self.fields)[idx]).name) == (name)):
                return (self.fields)[idx]

            idx = (idx) + (1)

        return _cast(None, lambda: Field)

    def getMethods(self):
        return self.methods

    def getMethod(self, name):
        idx = 0;
        while ((idx) < (len(self.methods))):
            if ((((self.methods)[idx]).name) == (name)):
                return (self.methods)[idx]

            idx = (idx) + (1)

        return _cast(None, lambda: Method)

    def isSubclassOf(self, anotherClass):
        if ((anotherClass) == (self)):
            return True

        idx = 0;
        while ((idx) < (len((self).parents))):
            if ((Class.get(((self).parents)[idx])).isSubclassOf(anotherClass)):
                return True

            idx = (idx) + (1)

        return False

    def hasInstance(self, o):
        """
        Return whether the given object is an instance of the class or one of its super-classes.
        """
        if ((o) == (None)):
            return False

        instanceClass = Class.get(_getClass(o));
        if ((instanceClass) == (None)):
            return False

        return (Class.get(_getClass(o))).isSubclassOf(self)

    def _getClass(self):
        return u"quark.reflect.Class"

    def _getField(self, name):
        if ((name) == (u"classes")):
            return Class.classes

        if ((name) == (u"VOID")):
            return Class.VOID

        if ((name) == (u"BOOL")):
            return Class.BOOL

        if ((name) == (u"INT")):
            return Class.INT

        if ((name) == (u"LONG")):
            return Class.LONG

        if ((name) == (u"FLOAT")):
            return Class.FLOAT

        if ((name) == (u"STRING")):
            return Class.STRING

        if ((name) == (u"OBJECT")):
            return Class.OBJECT

        if ((name) == (u"ERROR")):
            return Class.ERROR

        if ((name) == (u"id")):
            return (self).id

        if ((name) == (u"name")):
            return (self).name

        if ((name) == (u"parameters")):
            return (self).parameters

        if ((name) == (u"fields")):
            return (self).fields

        if ((name) == (u"methods")):
            return (self).methods

        if ((name) == (u"parents")):
            return (self).parents

        return None

    def _setField(self, name, value):
        if ((name) == (u"classes")):
            Class.classes = _cast(value, lambda: _Map)

        if ((name) == (u"VOID")):
            Class.VOID = _cast(value, lambda: Class)

        if ((name) == (u"BOOL")):
            Class.BOOL = _cast(value, lambda: Class)

        if ((name) == (u"INT")):
            Class.INT = _cast(value, lambda: Class)

        if ((name) == (u"LONG")):
            Class.LONG = _cast(value, lambda: Class)

        if ((name) == (u"FLOAT")):
            Class.FLOAT = _cast(value, lambda: Class)

        if ((name) == (u"STRING")):
            Class.STRING = _cast(value, lambda: Class)

        if ((name) == (u"OBJECT")):
            Class.OBJECT = _cast(value, lambda: Class)

        if ((name) == (u"ERROR")):
            Class.ERROR = _cast(value, lambda: Class)

        if ((name) == (u"id")):
            (self).id = _cast(value, lambda: unicode)

        if ((name) == (u"name")):
            (self).name = _cast(value, lambda: unicode)

        if ((name) == (u"parameters")):
            (self).parameters = _cast(value, lambda: _List)

        if ((name) == (u"fields")):
            (self).fields = _cast(value, lambda: _List)

        if ((name) == (u"methods")):
            (self).methods = _cast(value, lambda: _List)

        if ((name) == (u"parents")):
            (self).parents = _cast(value, lambda: _List)


Class.classes = {}
Class.VOID = Class(u"quark.void")
Class.BOOL = Class(u"quark.bool")
Class.INT = Class(u"quark.int")
Class.LONG = Class(u"quark.long")
Class.FLOAT = Class(u"quark.float")
Class.STRING = Class(u"quark.String")
Class.OBJECT = Class(u"quark.Object")
Class.ERROR = None
class Field(_QObject):
    def _init(self):
        self.type = None
        self.name = None

    def __init__(self, type, name):
        self._init()
        (self).type = type
        (self).name = name

    def getType(self):
        return Class.get(self.type)

    def getName(self):
        return self.name

    def _getClass(self):
        return u"quark.reflect.Field"

    def _getField(self, name):
        if ((name) == (u"type")):
            return (self).type

        if ((name) == (u"name")):
            return (self).name

        return None

    def _setField(self, name, value):
        if ((name) == (u"type")):
            (self).type = _cast(value, lambda: unicode)

        if ((name) == (u"name")):
            (self).name = _cast(value, lambda: unicode)



class Method(_QObject):
    def _init(self):
        self.type = None
        self.name = None
        self.parameters = None

    def __init__(self, type, name, parameters):
        self._init()
        (self).type = type
        (self).name = name
        (self).parameters = parameters

    def getType(self):
        return Class.get(self.type)

    def getName(self):
        return self.name

    def getParameters(self):
        result = _List([]);
        idx = 0;
        while ((idx) < (len(self.parameters))):
            (result).append(Class.get((self.parameters)[idx]));
            idx = (idx) + (1)

        return result

    def invoke(self, object, args):
        raise NotImplementedError('`Method.invoke` is an abstract method')

    def _getClass(self):
        return u"quark.reflect.Method"

    def _getField(self, name):
        if ((name) == (u"type")):
            return (self).type

        if ((name) == (u"name")):
            return (self).name

        if ((name) == (u"parameters")):
            return (self).parameters

        return None

    def _setField(self, name, value):
        if ((name) == (u"type")):
            (self).type = _cast(value, lambda: unicode)

        if ((name) == (u"name")):
            (self).name = _cast(value, lambda: unicode)

        if ((name) == (u"parameters")):
            (self).parameters = _cast(value, lambda: _List)



_lazyImport.pump("quark.reflect")

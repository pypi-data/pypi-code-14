import inspect
import new
from threading import RLock

from ContextBean import ContextBean

cacheLock = RLock()
def getSimpleNameFromString(obj):
    return obj.split(".")[-1]

def __getSimpleClassNameFromObjectInner(obj):
    """returns class name (without package for given object)"""
    # type: (object) -> str
    tp = type(obj)
    if tp is new.classobj or tp is type:
        return getSimpleNameFromString(obj.__name__)
    elif tp is str:
        return obj
    elif tp is new.instance:
        return getSimpleNameFromString(obj.__class__.__name__)
    raise Exception("Cannot get className for object:" + str(type(obj)))


def getSimpleClassNameFromObject(obj):
    """returns class name (without package for given object)"""
    # type: (object) -> str
    cacheLock.acquire()
    try:
        if not hasattr(obj, "__simpleClassName"):
            obj.__simpleClassName = __getSimpleClassNameFromObjectInner(obj)
    finally:
        cacheLock.release()
    return obj.__simpleClassName



def getObjectPackage(obj):
    # type: (object) -> str
    """returns object package"""
    if type(obj) is str:
        return obj
    if not hasattr(obj, "__module__"):
        if type(obj).__name__ == 'module':
            possibleError = "Type to inject is module, mb you imported/injected module instead of class: {obj}".format(obj=obj)
        else:
            possibleError = "unknown"

        raise Exception("Error, object has no attribute __module__:{obj}, type:{type}, possible error:{possibleError}".format(obj=obj, type=type(obj), possibleError = possibleError))
    return obj.__module__


def __getFullyQualifiedNameInner(obj):
    # type: (object) -> str
    """returns class name with package"""
    result = []
    package = getObjectPackage(obj)
    if package:
        result.append(package)
    result.append(getSimpleClassNameFromObject(obj))
    return ".".join(result)

def getFullyQualifiedName(obj):
    # type: (object) -> str
    """returns class name with package"""
    if type(obj) is str:
        return obj
    cacheLock.acquire()
    try:
        if not hasattr(obj, "__fullyQualifiedClassName"):
            obj.__fullyQualifiedClassName = __getFullyQualifiedNameInner(obj)
    finally:
        cacheLock.release()
    return obj.__fullyQualifiedClassName

def getScope(scopeHolder):
    if hasattr(scopeHolder, "TTTcontextScope"):
        return scopeHolder.TTTcontextScope
    raise Exception("Error, object is not scopeHolder:" + (str(scopeHolder)))

def getClassMethods(cls):
    # type: (object) -> list[object]
    return map(lambda meth: meth[1], inspect.getmembers(cls, predicate=inspect.ismethod))

def beanAnnotateMethod(method, annotation):
    cacheLock.acquire()
    try:
        if not hasattr(method, "TTTannotations"):
            method.TTTannotations = []
        if annotation in method.TTTannotations:
            raise Exception("Error, method: {methodName} already has annotation: {annotationName}".format(methodName=method.__name__,annotationName=annotation.__name__))
        method.TTTannotations.append(annotation)
    finally:
        cacheLock.release()

def getBeanMethodsInitializers(clazz):
    # type: (object) -> dict[object, object]
    cacheLock.acquire()
    try:
        if hasattr(clazz, "__annotatedMethods"):
            return clazz.__annotatedMethods
        methods = {}
        for method in getClassMethods(clazz):
            if hasattr(method, "TTTannotations"):
                methods[method] = method.TTTannotations
        clazz.__annotatedMethods = methods
        return methods
    finally:
        cacheLock.release()

def createBean(clazz, lazy=True):
    bean = ContextBean()
    bean.lazy = lazy
    bean.name = getFullyQualifiedName(clazz)
    bean.object = clazz
    return bean
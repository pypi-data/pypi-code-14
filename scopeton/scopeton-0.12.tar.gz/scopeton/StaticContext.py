import copy
from threading import RLock

import DiTools
from ContextBean import ContextBean

lock = RLock()
def _StaticSync(fn):
    def wrapped(*args, **kwargs):
        lock.acquire()
        try:
            return fn(*args, **kwargs)
        finally:
            lock.release()
    return wrapped


class StaticContext(object):
    _beans = {}  # type: dict[str, object]
    @classmethod
    @_StaticSync
    def getBeansCopy(cls):
        return copy.copy(cls._beans)

    @classmethod
    @_StaticSync
    def registerBean(cls, clazz, lazy = True):
        # type: (str, ContextBean) -> object
        bean = ContextBean()
        bean.lazy = lazy
        bean.name = DiTools.getFullyQualifiedName(clazz)
        bean.object = clazz
        cls.annotations = DiTools.getBeanMethodsInitializers(clazz)
        cls._beans[bean.name] = bean

def Service(lazy = True):
    def decorator(cls):
        StaticContext.registerBean(cls, lazy=lazy)
        return cls
    return decorator
from threading import RLock

import DiTools
from ContextBean import ContextBean

class ScopeContext(object):
    def __init__(self, beans, servicesAutoStart=True):
        # type: (dict[str, ContextBean], boolean) -> object
        self.__instances = {}  # type: dict[str, object]
        self.scopeLock = RLock()
        self.beans = beans  # type: (dict[str, ContextBean]) -> object
        if servicesAutoStart:
            self.startServices()

    def startServices(self):
        for serviceQualifier in self.beans:
            if not self.beans[serviceQualifier].lazy:
                self.getInstance(self.beans[serviceQualifier].object)

    def resolveClass(self, name):
        # type: (object) -> ContextBean
        pkg = DiTools.getFullyQualifiedName(name)
        if pkg not in self.beans:
            raise Exception("Error, no class with name {pkg} registered, available:{keys}".format(pkg=pkg, keys=self.beans.keys()))
        return self.beans[pkg]

    def __initInstance(self, instance):
        instance.TTTcontextScope = self
        if hasattr(instance, "TTTinjectMethod"):
            instance.TTTinjectMethod()
        annotatedMethods = DiTools.getBeanMethodsInitializers(instance.__class__)
        for method in annotatedMethods:
            for annorarionInitFunction in annotatedMethods[method]:
                annorarionInitFunction(instance)
        return instance

    def _makeInstance(self, cls):
        # type: (ContextBean) -> object
        return self.__initInstance(cls.object())

    def registerInstance(self, name, instance):
        self.__instances[DiTools.getFullyQualifiedName(name)] = instance
        return self.__initInstance(instance)

    def registerBean(self, name, cls):
        self.beans[DiTools.getFullyQualifiedName(name)] = DiTools.createBean(cls)

    def getInstance(self, obj):
        name = DiTools.getFullyQualifiedName(obj)
        if name in self.__instances:
            return self.__instances[name]
        cls = self.resolveClass(obj)
        self.scopeLock.acquire()
        try:
            if name not in self.__instances:
                self.__instances[name] = self._makeInstance(cls)
        finally:
            self.scopeLock.release()
        return self.__instances[name]

    def destroyInstance(self, instance):
        if hasattr(instance, "TTTPreDestroy"):
            instance.TTTPreDestroy()

    def destroy(self):
        self.scopeLock.acquire()
        try:
            for name in self.__instances:
                instance = self.__instances[name]
                self.destroyInstance(instance)
        finally:
            self.scopeLock.release()
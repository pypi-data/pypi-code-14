from threading import RLock

class Scope(object):
    def __init__(self):
        self.__objects={}
        self.__instances={}
        self.scopeLock=RLock()

    def __getName(self, obj):
        if type(obj).__name__ == "str":
            return obj
        return obj.__name__.split(".")[-1]

    def get(self, name):
        self.scopeLock.acquire()
        try:
            name = self.__getName(name)
            return self.__objects[name]
        finally:
            self.scopeLock.release()


    def registerService(self, name, service):
        name = self.__getName(name)
        self.scopeLock.acquire()
        try:
            if name in self.__objects:
                raise Exception("Error, service {name} already exists".format(name=name))
            self.__objects[name] = service
        finally:
            self.scopeLock.release()

    def getInstance(self, name):
        name = self.__getName(name)
        if name in self.__instances:
            return self.__instances[name]
        self.scopeLock.acquire()
        if not name in self.__instances:
            self.__instances[name] = self.__objects[name]()
        self.scopeLock.release()
        return self.__instances[name]



    def registerInstance(self, name, instance):
        name = self.__getName(name)
        if name in self.__instances:
            raise Exception("Error, instance for {name} already exists".format(name=name))
        self.__instances[name] = instance



class Locator(object):
    scope=Scope()
    @staticmethod
    def registerService(service):
        Locator.scope.registerService(service, service)

    @staticmethod
    def registerInstance(instance, name=None):
        Locator.scope.registerInstance(name or instance.__class__, instance)

    @staticmethod
    def getInstance(service):
        return Locator.scope.getInstance(service)

def Inject(**kwargss):
    def decorator(fn):
        def wrapper(*args, **kwargs):
            for arg in kwargss:
                kwargs[arg] = Locator.getInstance(kwargss[arg])
            return fn(*args, **kwargs)
        return wrapper
    return decorator


def Service(*args, **kwargs):
    def decorator(cls):
        Locator.registerService(cls)
        return cls
    return decorator
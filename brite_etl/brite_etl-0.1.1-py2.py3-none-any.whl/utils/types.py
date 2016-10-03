from pydash import deep_has, deep_get, deep_set, assign


class SingletonType(type):
    """
        Easy singleton - http://amir.rachum.com/blog/2012/04/26/implementing-the-singleton-pattern-in-python/
    """
    def __call__(cls, *args, **kwargs):
        try:
            return cls.__instance
        except AttributeError:
            cls.__instance = super(SingletonType, cls).__call__(*args, **kwargs)
            return cls.__instance


class DeepDict(dict):
    def __init__(self, *args, **kwargs):
        self.update(*args, **kwargs)

    def get(self, key):
        return deep_get(self, key)

    def set(self, key, value):
        assign(self, deep_set(self, key, value))
        return self

    def has(self, key):
        return deep_has(self, key)

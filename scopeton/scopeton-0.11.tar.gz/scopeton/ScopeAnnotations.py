from scopeton import DiTools

def InjectClass(**kwargs_):
    def decorator(cls):
        def inject(self):
                for name in kwargs_:
                    try:
                        setattr(self, name, self.TTTcontextScope.getInstance(kwargs_[name]))
                    except Exception as e:
                        raise Exception("Error while injecting {name} into {cls}, type is: {obj}".format(name=name, cls = cls, obj = kwargs_[name]), e)

        cls.TTTinjectMethod = inject
        return cls
    return decorator

def PostConstruct():
    """
    method marked by postConstruct will be called on bean initialization
    :return:
    """
    def decorator(fn):
        def initAnnotation(self):
            fn(self)
        DiTools.beanAnnotateMethod(fn, initAnnotation)
        return fn
    return decorator

def PreDestroy():
    def decorator(fn):
        def initAnnotation(self):
            self.TTTPreDestroy = fn
        DiTools.beanAnnotateMethod(fn, initAnnotation)
        return fn
    return decorator
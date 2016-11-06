from scopeton import DiTools

def InjectClass(**kwargs_):
    def decorator(cls):
        def inject(self):
            for name in kwargs_:
                setattr(self, name, self.TTTcontextScope.getInstance(kwargs_[name]))
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
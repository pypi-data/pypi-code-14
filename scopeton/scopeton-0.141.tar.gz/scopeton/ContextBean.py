class ContextBean(object):
    name = ""
    object = None  # type: object
    postConstruct = None
    preDestroy = None
    lazy = False
    def __str__(self):
        return "ContextBean[{self.name}](lazy={self.lazy})".format(self=self)
    def __repr__(self):
        return self.__str__()
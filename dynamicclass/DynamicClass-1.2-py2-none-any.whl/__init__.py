class DynamicClass():
    def __getattr__(self, item):
        newobj = self.__class__()
        setattr(self, item, newobj)
        return newobj

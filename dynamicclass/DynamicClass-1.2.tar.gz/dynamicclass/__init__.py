class DynamicClass():

    def from_list(self, mylist):
        lista = []
        for v in mylist:
            if isinstance(v, dict):
                v = DynamicClass(**v)
            elif isinstance(v, list):
                v = self.from_list(v)

            lista.append(v)
        return lista

    def __init__(self, **kwargs):

        for key, value in kwargs.items():
            if isinstance(value, dict):
                value = DynamicClass(**value)
            elif isinstance(value, list):
                mylist = []
                for v in value:
                    if isinstance(v, dict):
                       v = DynamicClass(**v)
                    elif isinstance(v, list):
                       v = self.from_list(v)

                    mylist.append(v)
                value = mylist

            setattr(self, key, value)

    def __getattr__(self, item):
        newobj = self.__class__()
        setattr(self, item, newobj)
        return newobj

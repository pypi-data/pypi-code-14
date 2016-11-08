import os, re


class Path:
    def __init__(self, path):
        """Create a Path object to represent a
        file path. Made for all the file classes
        in order to make them easier to usee."""
        self.__path = os.path.abspath(path)
        self.__name = os.path.basename(path)
        print(self.__name)

    def __getattribute__(self, item):
        if item == 'name' and self.__name == '':
            raise AttributeError("AttributeError: 'Path' object has no attribute 'name'")
        return super().__getattribute__(item)

    def path(self, folder=False):
        return re.sub(self.__name, '', self.__path) if folder else self.__path

    def name(self, no_ext=False):
        return re.sub('\.\w+', '', self.__name) if no_ext else self.__name

    @property
    def exist(self):
        return os.path.exists(self.__path)

    @property
    def size(self):
        return os.path.getsize(self.__path)
    def full(self,no_ext=False):
        print(self.path(folder=True)+self.name(no_ext=True))
        return self.path(folder=True)+self.name(no_ext=True)if no_ext else self.__path

    def __str__(self):
        return self.path()

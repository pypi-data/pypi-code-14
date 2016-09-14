from abc import ABCMeta
from abc import abstractmethod

# ToDo
class PowerOperationsInterface(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def shutdown(self):
        pass

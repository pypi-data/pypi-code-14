from abc import ABCMeta, abstractmethod
from yapsy.IPlugin import IPlugin


class IStorageProvider(IPlugin, metaclass=ABCMeta):
    @abstractmethod
    def name(self) -> str:
        pass

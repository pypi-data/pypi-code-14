from abc import ABCMeta, abstractmethod
from yapsy.IPlugin import IPlugin


class IFilesystem(IPlugin, metaclass=ABCMeta):
    @abstractmethod
    def name(self) -> str:
        pass

    @abstractmethod
    def create(self, ciphertextDir: str, plaintextDir: str, password: bytes) -> None:
        pass


class FilesystemCreateException(Exception):
    def __init__(self, message: str) -> None:
        self._message = message

    def message(self) -> str:
        return self._message

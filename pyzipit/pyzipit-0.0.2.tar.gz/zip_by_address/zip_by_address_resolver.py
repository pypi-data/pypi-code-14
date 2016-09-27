from abc import ABCMeta, abstractmethod


class ZipByAddressResolver(metaclass=ABCMeta):
    def __init__(self, address):
        self._address = address
        self._validate_address()

    def resolve_zip(self):
        return self._resolve_zip_from_validated_address()

    def __str__(self):
        return '{}: {}'.format(self.__class__.__name__, self._address)

    @abstractmethod
    def _validate_address(self):
        pass

    @abstractmethod
    def _resolve_zip_from_validated_address(self):
        pass

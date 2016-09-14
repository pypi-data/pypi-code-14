from abc import ABCMeta
from abc import abstractmethod


class FirmwareOperationsInterface(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def load_firmware(self, path, vrf_management_name):
        pass

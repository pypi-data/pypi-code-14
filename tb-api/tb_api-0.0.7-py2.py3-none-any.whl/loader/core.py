from abc import ABCMeta, abstractmethod


class Loader(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def get_method(self, module_name, method_name):
        pass

    def json_dump_cls(self):
        return None

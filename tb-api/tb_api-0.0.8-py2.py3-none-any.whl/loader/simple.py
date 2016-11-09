# encoding=utf-8
import traceback
from importlib import import_module

from tb_api.exception import ImportModuleError, ImportModuleClassError, InvalidMethodError
from tb_api.loader.core import Loader


class LoaderSimple(Loader):
    def __init__(self, base_name, module_suffix=""):
        self.module_suffix = module_suffix
        self.base_name = base_name
        self.cache = {}
        self.cache_module = {}

    def get_method(self, module_name, method_name):
        key = module_name + ":" + method_name
        if key not in self.cache:
            obj = self.get_obj(module_name)
            try:
                method = getattr(obj, method_name)
            except AttributeError:
                raise InvalidMethodError(module_name, method_name)

            self.cache[key] = method

        return self.cache[key]

    def get_obj(self, module_name):
        if module_name not in self.cache_module:
            actual_module_name = '{0}{1}'.format(module_name, self.module_suffix)
            module_full_name = '{0}.{1}'.format(self.base_name, actual_module_name)
            try:
                module = import_module(module_full_name)
            except ImportError as e:
                print(traceback.format_exc())
                raise ImportModuleError(module_full_name, str(e), traceback.format_exc())

            # print(module_full_name, module_name)
            # print(module)

            try:
                clazz = getattr(module, actual_module_name)
            except AttributeError:
                raise ImportModuleClassError(module_full_name, actual_module_name)

            self.cache_module[module_name] = clazz()

        return self.cache_module[module_name]

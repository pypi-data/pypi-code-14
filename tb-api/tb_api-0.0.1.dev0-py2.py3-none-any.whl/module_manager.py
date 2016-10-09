# encoding=utf-8
from importlib import import_module


class ModuleManager(object):
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
                raise Exception("Invalid method", module_name, method_name)

            self.cache[key] = method

        return self.cache[key]

    def get_obj(self, module_name):
        if module_name not in self.cache_module:
            actual_module_name = '{0}{1}'.format(module_name, self.module_suffix)
            module_full_name = '{0}.{1}'.format(self.base_name, actual_module_name)
            try:
                module = import_module(module_full_name)
            except ImportError:
                raise Exception("Import error", module_full_name)

            # print(module_full_name, module_name)
            # print(module)

            clazz = getattr(module, actual_module_name)

            self.cache_module[module_name] = clazz()

        return self.cache_module[module_name]

from tb_ioc import IOC

from tb_api.loader.core import Loader


class LoaderIOC(Loader):
    def __init__(self, config_files, module_suffix=''):
        self.module_suffix = module_suffix
        self.ioc = IOC()
        for config_file in config_files:
            self.ioc.load_file(config_file)

        if not module_suffix:
            self.module_suffix = self.ioc.get_parameter('API_ModulePrefix')

        self._cache_methods = {}

    def get_method(self, module_name, method_name):
        key = '%s-%s' % (module_name, method_name)
        if key not in self._cache_methods:
            service_name = '%s%s' % (module_name, self.module_suffix)
            obj = self.ioc.get(service_name)
            method = getattr(obj, method_name)

            self._cache_methods[key] = method
        return self._cache_methods[key]

    def json_dump_cls(self):
        return self.ioc.get_parameter('API_Dumper')


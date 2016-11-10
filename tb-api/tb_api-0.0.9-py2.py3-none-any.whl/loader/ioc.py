from tb_ioc import IOC

from tb_api.exception import UnauthorizedError
from tb_api.loader.core import Loader
from tb_api.model import APIConfig


class LoaderIOC(Loader):
    def __init__(self, config_files, module_suffix=''):
        self.module_suffix = module_suffix
        self.ioc = IOC()
        for config_file in config_files:
            self.ioc.load_file(config_file)

        if not module_suffix:
            self.module_suffix = self.ioc.get_parameter('API_ModuleSuffix')

        self.config = APIConfig(self.ioc.get_parameter('API_Config', {}))
        self._cache_methods = {}

    def get_method(self, module_path, method_path):
        key = '%s-%s' % (module_path, method_path)
        if key not in self._cache_methods:
            method_config = self.config.get_config(module_path, method_path)
            if not method_config:
                raise UnauthorizedError(module_path, method_path)

            service_name = '%s%s' % (method_config.module_name, self.module_suffix)
            obj = self.ioc.get(service_name)
            method = getattr(obj, method_path)

            self._cache_methods[key] = method
        return self._cache_methods[key]

    def json_dump_cls(self):
        return self.ioc.get_parameter('API_Dumper')

    def secret_key(self):
        return self.ioc.get_parameter('API_SecretKey')

    def get_app_handlers(self):
        handler_names = self.ioc.get_parameter('API_AppHandler')
        ret = []
        for name in handler_names:
            ret.append(self.ioc.get(name))

        return ret

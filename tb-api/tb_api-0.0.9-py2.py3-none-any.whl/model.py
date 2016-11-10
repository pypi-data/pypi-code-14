from os.path import abspath


class Config(object):
    def __init__(self, project_dir, debug, port):
        self.debug = debug
        self.project_dir = abspath(project_dir)
        self.port = port
        self.loader = None


class APIMethodConfig(object):
    def __init__(self, module_name, method_name, fields, tags=[], http_methods=[]):
        self.tags = tags
        self.module_name = module_name
        self.method_name = method_name
        self.fields = fields
        self.http_methods = http_methods


class APIFieldConfig(object):
    def __init__(self, config):
        self.name = config['name']
        self.description = config.get('description', '')
        self.required = config.get('required', True)
        self.type = config.get('type', 'string')
        self.defaultValue = config.get('default')


class APIConfig(object):
    def __init__(self, data):
        self.data = data

        self.path_map = {}

        services = data.get('services', {})
        for module_name in services:
            module_config = services[module_name]
            module_path = module_config.get('path', module_name)
            if module_path not in self.path_map:
                self.path_map[module_path] = {}

            methods = module_config.get('methods', {})
            tags = module_config.get('tags', [])

            for method_name in methods:
                method_config = methods[method_name]
                method_path = method_config.get('path', method_name)
                fields = [APIFieldConfig(_) for _ in method_config.get('fields', [])]
                method_tags = tags + method_config.get('tags', [])
                http_methods = method_config.get('method', ['get'])

                method_config = APIMethodConfig(module_name, method_name, fields,
                                                tags=method_tags, http_methods=http_methods)

                self.path_map[module_path][method_path] = method_config

    def get_config(self, module_path, method_path):
        return self.path_map.get(module_path, {}).get(method_path)

import importlib

def resolve_func(func_string):
    module_name, func_name = func_string.rsplit(".", 1)
    module = importlib.import_module(module_name)
    func = getattr(module, func_name)

    if not func:
        raise ImportError(name=func_name, path=func_strung)

    return func

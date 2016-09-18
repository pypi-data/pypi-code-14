from importlib import import_module


def function_from_string(func_string):
    """
    Returns a function object from the function string.
    :param the string which needs to be resolved.
    """

    func = None
    func_string_splitted = func_string.split('.')
    module_name = '.'.join(func_string_splitted[:-1])
    function_name = func_string_splitted[-1]
    module = import_module(module_name)
    if module and function_name:
        func = getattr(module, function_name)
    return func

import numbers


def getPath(*args):
    obj = args[0]
    res = None
    for argK in xrange(1, len(args)):
        arg = args[argK]
        if (isinstance(obj, dict) and arg in obj) or \
                ((isinstance(obj, list) or isinstance(obj, set)) and (isinstance(arg, numbers.Number) and len(obj) > arg)):
            res = obj[arg]
            obj = res
        else:
            return None
    return res


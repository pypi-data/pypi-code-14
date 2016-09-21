def add_data(*args):
    listargs = [i for i in args]
    def func(i):
        if isinstance(i, list):
            return i + listargs
        return [i] + listargs
    return func

def add_data(*args):
    def func(i):
        if isinstance(i, list):
            return i + args
        return [i] + args
    return func

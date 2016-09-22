def remove_data(*args):
    def func(i):
        for key in args:
            i.pop(key, None)
        if len(i.keys()) is 1:
            return i[i.keys()[0]]
        return i
    return func

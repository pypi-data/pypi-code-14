def remove_data(*args):
    def func(i):
        for key in args:
            i.pop(key, None)
        if len(i.keys()) is 1:
            return list(i.values())[0]
        return i
    return func

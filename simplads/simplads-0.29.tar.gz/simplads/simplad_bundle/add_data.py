def add_data(*args):
    keys = [i for i in args][::2]
    vals = [i for i in args][1::2]
    def func(i):
        for a in len(keys):
            i[keys[a]] = vals[a]
        return i
    return func

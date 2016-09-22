def add_first_data(key, *args):
    keys = [i for i in args][::2]
    vals = [i for i in args][1::2]
    def func(i):
        i = {key: i}
        for a, key in keys:
            i[key] = vals[a]
        return i
    return func

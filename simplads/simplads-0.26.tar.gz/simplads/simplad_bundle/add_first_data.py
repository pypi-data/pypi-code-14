def add_first_data(key, *args):
    stored_key = key
    keys = [i for i in args][::2]
    vals = [i for i in args][1::2]
    def func(i):
        i = {stored_key: i}
        for a, key in keys.items():
            i[key] = vals[a]
        return i
    return func

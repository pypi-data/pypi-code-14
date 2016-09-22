def add_first_data(key, *args):
    stored_key = key
    keys = [i for i in args][::2]
    vals = [i for i in args][1::2]
    def func(i):
        i = {stored_key: i}
        for a in count(keys):
            i[keys[a]] = vals[a]
        return i
    return func

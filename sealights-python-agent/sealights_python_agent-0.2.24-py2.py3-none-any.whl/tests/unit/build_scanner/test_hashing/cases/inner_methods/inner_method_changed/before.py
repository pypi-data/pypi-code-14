
def outside_method(a, b):
    def inner_method(c, d):
        return c + d
    return inner_method(a, b)


def outside_method(a, b):
    def inner_method(c, d):
        return abs(1)
    return inner_method(a, b)

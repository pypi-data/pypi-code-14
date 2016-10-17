
def outside_method(a, b):
    def inner_method(c, d):
        return str(1)
    return inner_method(a, b)

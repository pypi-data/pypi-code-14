class Pair:
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def __str__(self):
        return '%s <---> %s' % (self.a.name, self.b.name)

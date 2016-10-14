class Column(object):

    def __init__(self, name, key, width=None):
        self.name = name
        self.set_get_attr_for(key)
        self.width = width

    def set_get_attr_for(self, key):
        if not callable(key):
            raise Exception('key need be callable')
        self.get_attr_for = key

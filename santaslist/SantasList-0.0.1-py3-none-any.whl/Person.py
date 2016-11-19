class Person:
    def __init__(self, dict):
        self.name = dict['name']
        self.username = dict['username']

    def __str__(self):
        return '%s (%s)' % (self.name, self.username)
